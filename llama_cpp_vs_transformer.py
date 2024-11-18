import time
import torch

from llama_cpp import Llama
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

llm = Llama(
        model_path = "/path/to/model/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf",
        n_ctx=2048,
        n_gpu_layers = -1,
)

llama_model_id = "/path/to/model/Llama-3.1-8B-Instruct"
llama_device = "cuda"
llama_dtype = torch.bfloat16
pipe = pipeline(
    "text-generation",
    model=llama_model_id,
    model_kwargs={"torch_dtype": llama_dtype},
    device_map="auto",
)

system_prompt_llm = "You are an assistant that knows machine learning."

while True:
    text = input(f"\n\nEnter:")

    messages = [
    {f"role": "system", "content": {system_prompt_llm}},
    {f"role": "user", "content": {text}}
    ]

    t0 = time.time() 
    output = llm.create_chat_completion(
        messages,
        max_tokens=1024,
        temperature=0.6,
        #stop=["Q", "\n"],
        top_p=0.9,
        top_k=4,
        repeat_penalty=1.1
    )
    print(output["choices"][0]["message"]["content"])
    t1 = time.time()        
    print("\nllama.cpp Response time: ", t1 - t0)

    t2 = time.time()        
    

    pad_token_id = pipe.tokenizer.pad_token_id
    terminators = [
        pipe.tokenizer.eos_token_id,
        pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipe(
        messages,
        max_new_tokens=1024,
        pad_token_id=pad_token_id,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        top_k=4,
        repetition_penalty=1.1,
        return_full_text=False
    )
    assistant_response = outputs[0]["generated_text"]
    print(f"\n{assistant_response}")
    t3 = time.time() 
    print("\ntransformers Response time: ", t3 - t2)
