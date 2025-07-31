import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os
from typing import Optional

class PortfolioLLMService:
    def __init__(self, model_path: str = "portfolio-llm-final"):
        self.model_path = model_path
        self.base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def load_model(self):
        """Load the fine-tuned PEFT model and tokenizer"""
        try:
            print(f"🤖 Loading PEFT adapter from {self.model_path}...")
            
            # Check multiple possible paths for the adapter
            possible_paths = [
                os.path.join("trained_models", self.model_path),
                os.path.join("./trained_models", self.model_path),
                os.path.join("../portfolio-llm/trained_models", self.model_path),
                self.model_path
            ]
            
            adapter_path = None
            for path in possible_paths:
                if os.path.exists(path) and os.path.exists(os.path.join(path, "adapter_config.json")):
                    adapter_path = path
                    break
            
            if not adapter_path:
                raise FileNotFoundError(f"PEFT adapter not found in any of these paths: {possible_paths}")
            
            print(f"✅ Found PEFT adapter at: {adapter_path}")
            
            # Load base model first
            print(f"Loading base model: {self.base_model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float32,  # Use float32 for CPU
                device_map=None
            )
            
            # Load PEFT adapter
            print("Loading PEFT adapter...")
            self.model = PeftModel.from_pretrained(base_model, adapter_path)
            
            if not torch.cuda.is_available():
                self.model = self.model.to("cpu")
                
            print(f"✅ PEFT model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading PEFT model: {str(e)}")
            return False
    
    def generate_response(self, message: str, max_tokens: int = 200, temperature: float = 0.7) -> str:
        """Generate response using the loaded PEFT model"""
        if not self.model or not self.tokenizer:
            return "Error: Model not loaded"
        
        try:
            # Format prompt similar to training data
            prompt = f"### Instruction:\nAnswer the following question about Arun's resume.\n### Input:\n{message}\n### Response:\n"
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the response part
            if "### Response:" in response:
                answer = response.split("### Response:")[-1].strip()
            else:
                answer = response.strip()
            
            return answer
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"

# Global service instance
llm_service_instance: Optional[PortfolioLLMService] = None

def initialize_llm_service() -> Optional[PortfolioLLMService]:
    """Initialize the LLM service"""
    global llm_service_instance
    
    try:
        llm_service_instance = PortfolioLLMService()
        success = llm_service_instance.load_model()
        
        if success:
            return llm_service_instance
        else:
            print("⚠️ LLM service failed to initialize, falling back to external API")
            return None
            
    except Exception as e:
        print(f"⚠️ LLM service initialization error: {str(e)}")
        return None

def get_llm_response(message: str) -> str:
    """Get response from LLM service"""
    if llm_service_instance:
        return llm_service_instance.generate_response(message)
    else:
        return "LLM service not available"

