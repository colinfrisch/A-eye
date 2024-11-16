from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from PIL import Image
import requests, torch, os, time, warnings
warnings.filterwarnings("ignore")


"""
cd D:\hackathon
conda activate molmo

"""
pre = time.time()
# load the processor
processor = AutoProcessor.from_pretrained(
    'allenai/MolmoE-1B-0924',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto',
)

# load the model
model = AutoModelForCausalLM.from_pretrained(
    'allenai/MolmoE-1B-0924',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto',
)

print('model loaded /',time.time()-pre)



#___________________________________________

file_list = os.listdir('imgTest')
tl = []

for image in file_list :
    print("processing", image,"----------------------------------------------")

    img_path = os.path.join('imgTest',image)
    # process the image and text
    inputs = processor.process(
        images=[Image.open(img_path)],
        text="I'm a blind man and you're my visual guide, what should I know from this situation ? Your answer should be short and efficient."
    )

    # move inputs to the correct device and make a batch of size 1
    inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}

    start=time.time()
    # generate output; maximum 200 new tokens; stop generation when <|endoftext|> is generated
    output = model.generate_from_batch(
        inputs,
        GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
        tokenizer=processor.tokenizer
    )

    # only get generated tokens; decode them to text
    generated_tokens = output[0,inputs['input_ids'].size(1):]
    generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

    tl.append(time.time()-start)
    print(time.time()-start)
    # print the generated text
    print(generated_text)

print('time : ', tl)
    

