# data/

**Nada aqui é versionado.** O `.gitignore` bloqueia o conteúdo destas pastas de propósito:
datasets em Git incham o repositório e frequentemente violam a licença da fonte.

| Pasta | Conteúdo |
|---|---|
| `raw/` | arquivo original, exatamente como baixado da fonte — nunca editado |
| `processed/` | saída dos notebooks de pré-processamento (`.parquet` ou `.csv`) |

Documente abaixo como obter os dados brutos, para que qualquer pessoa consiga reproduzir o projeto.

## Como obter

1. Baixe o arquivo compactado em: https://drive.google.com/file/d/1UGLHJc6nqCQ-_oW24up37rVnxe4dInWQ/view?usp=sharing
2. Extrair os dois arquivos csv do zip no diretório: `data/raw/`  
