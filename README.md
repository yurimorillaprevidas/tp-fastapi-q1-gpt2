# Parte 1 - Questão 1 - Geração com GPT-2

Continua uma frase com o GPT-2 do Hugging Face.

## Como executar

Use Python 3.12. Se já descompactou o projeto, entre na pasta e pule a etapa de clonagem.

```bash
git clone https://github.com/yurimorillaprevidas/tp-fastapi-q1-gpt2.git
cd tp-fastapi-q1-gpt2
```

Crie e ative um ambiente virtual.

No Windows, use o PowerShell.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux, rode os comandos abaixo.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Em Windows ou Linux, instale primeiro a edição para CPU do PyTorch. No macOS, vá direto à instalação das dependências.

```bash
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
```

Instale as dependências.

```bash
python -m pip install -r requirements.txt
```

Inicie o servidor.

```bash
python -m uvicorn main:app
```

Na primeira execução, aguarde o download do modelo e o carregamento em memória. Os pesos ficam no cache local do Hugging Face. O servidor fica em `http://127.0.0.1:8000`.

## Como testar

Abra [a documentação interativa](http://127.0.0.1:8000/docs), selecione **POST /generate**, clique em **Try it out**, cole o JSON e clique em **Execute**.

```json
{
  "prompt": "The capital of France is"
}
```

Exemplo de resposta HTTP 200.

```json
{
  "generated_text": "The capital of France is Paris."
}
```

O campo `prompt` aceita até 2.000 caracteres, dentro da janela de contexto do GPT-2. A resposta inclui a frase original e até 48 tokens de continuação. O resultado pode variar.

O FastAPI retorna HTTP 422 se faltar o campo, se ele estiver vazio ou se exceder o limite.

[Documentação do modelo ou componente](<https://huggingface.co/openai-community/gpt2>)
