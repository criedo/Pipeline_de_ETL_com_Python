# Relato de Experiência — Desafio de Projeto "Explorando IA Generativa em um Pipeline de ETL com Python"

Olá, pessoal!

Gostaria de compartilhar meu relato de experiência ao desenvolver o **Desafio de Projeto "Explorando IA Generativa em um Pipeline de ETL com Python"**, proposto no **Bootcamp Santander de Ciência de Dados 2025**. Mais do que simplesmente seguir um notebook pronto, esse desafio acabou se tornando um excelente exercício de **raciocínio técnico, adaptação arquitetural e tomada de decisão**, muito parecido com o que enfrentamos no dia a dia profissional.


Durante o desenvolvimento deste desafio, optei por ir além da simples execução do notebook original, analisando o contexto técnico e as limitações reais do ambiente. Ao identificar que a API do Santander Dev Week estava descontinuada, adaptei a etapa de extração para trabalhar com dados locais, preservando a lógica do pipeline ETL. Da mesma forma, a API original da OpenAI utilizada no projeto encontrava-se obsoleta, o que exigiu a atualização para uma abordagem moderna e compatível. Nesse processo, escolhi utilizar a OpenRouter como alternativa, por permitir acesso a diferentes modelos de IA por meio de uma interface unificada e resiliente. Essa decisão reduziu o acoplamento do projeto a um único fornecedor e garantiu maior estabilidade à etapa de transformação. Mantive o foco na geração de mensagens curtas e personalizadas, conforme proposto no desafio, além de adicionar logs para melhor acompanhamento da execução. Por fim, a etapa de carga foi reinterpretada para um contexto local, assegurando que o fluxo de dados fosse concluído corretamente mesmo sem uma API ativa. Esse raciocínio permitiu manter o objetivo pedagógico do desafio e aproximar o exercício de um cenário real de engenharia de dados.

---

## Contexto do Desafio

A proposta original do desafio era bastante clara:

- Trabalhar um pipeline **ETL (Extract, Transform, Load)** em Python;
- Ler dados de usuários a partir de um CSV;
- Consumir uma API REST do Santander Dev Week 2023 para obter dados dos clientes;
- Utilizar **IA generativa** para criar mensagens personalizadas de marketing;
- Atualizar essas mensagens na API do Santander.

O foco pedagógico sempre foi o **entendimento do fluxo ETL aliado ao uso de IA**, e não necessariamente a integração em produção com serviços reais.

---

## Primeiro Desafio Real: APIs Fora do Ar

Ao executar o notebook, me deparei rapidamente com dois problemas importantes:

1. A **API pública do Santander Bootcamp 2025** estava descontinuada, impossibilitando tanto o `GET` quanto o `PUT` de usuários;
2. A **API antiga da OpenAI**, utilizada no notebook original (`openai.ChatCompletion.create`), havia sido removida nas versões mais recentes da biblioteca Python.

Esse foi o primeiro ponto em que ficou claro que o desafio exigia mais do que copiar e colar código: era necessário **entender o que estava sendo feito** para poder adaptar.

---

## Decisão Técnica: Preservar o ETL, Adaptar as Dependências

Em vez de tentar "forçar" soluções quebradas, optei por uma abordagem que considero mais alinhada com boas práticas:

- Manter o **objetivo conceitual do ETL**;
- Substituir apenas as **dependências externas indisponíveis**;
- Atualizar o código para padrões modernos e suportados.

Essa decisão foi essencial para não descaracterizar o desafio e, ao mesmo tempo, torná-lo executável.

---

## Ajustes na Etapa de Extract

Com a API do Santander fora do ar, a etapa de **Extract** foi adaptada para leitura direta de um CSV contendo `id` e `name` dos usuários.

Dessa forma, continuei trabalhando com uma fonte externa de dados, preservando a lógica do ETL, mas sem depender de um serviço indisponível.

---

## Transform: Da OpenAI para a OpenRouter

A etapa de **Transform** foi a mais interessante do ponto de vista técnico e onde concentrei a maior parte do raciocínio de adaptação.

Inicialmente, o notebook utilizava a API antiga da OpenAI (`openai.ChatCompletion.create`), que foi descontinuada. Em vez de apenas corrigir o erro, optei por uma solução mais robusta: integrar o projeto à **OpenRouter**, que funciona como um gateway unificado para múltiplos modelos de IA.

A grande vantagem dessa abordagem é reduzir o acoplamento com um único fornecedor e aumentar a resiliência do pipeline.

### Configuração do cliente OpenRouter

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
    default_headers={
        "HTTP-Referer": "https://colab.research.google.com",
        "X-Title": "Santander DIO 2025 - ETL"
    }
)
```

Nesse trecho:
- Reutilizo a **SDK moderna da OpenAI**;
- Apenas redireciono o `base_url` para a OpenRouter;
- Adiciono headers opcionais para identificação do projeto.

### Geração da mensagem com IA

```python
def generate_ai_news(user):
    print(f"[LOG] Gerando mensagem para {user['name']}...")

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Crie uma mensagem curta (máx. 100 caracteres) "
                    f"sobre investimentos para o cliente {user['name']}."
                )
            }
        ],
        max_tokens=80,
        temperature=0.7
    )

    message = response.choices[0].message.content.strip()
    return message
```

Aqui, o foco foi:
- Garantir **mensagens curtas**, conforme o desafio;
- Manter **logs claros** para observabilidade;
- Trabalhar com um modelo atual, válido e disponível.

---


## Load: Reinterpretando a Etapa Final

Como o endpoint `PUT` da API do Santander também não estava disponível, a etapa de **Load** precisou ser reinterpretada.

Em vez de atualizar uma API externa, os resultados finais passaram a ser:

- Impressos no console;
- Ou salvos localmente em CSV/JSON.

Isso manteve o princípio da etapa de Load — entregar os dados transformados a um destino — sem depender de uma infraestrutura que não existe mais.

---

## Resultados e Aprendizados

Ao final do desafio, consegui:

- Executar todo o pipeline ETL de ponta a ponta;
- Integrar IA generativa de forma funcional e atualizada;
- Trabalhar com APIs modernas e resilientes;
- Exercitar tomada de decisão técnica diante de limitações reais.

Mais importante do que o resultado final foi o aprendizado de que **engenharia de dados não é seguir tutoriais**, mas sim **entender o problema e adaptar a solução ao contexto**.

---

## Conclusão (Visão Técnica )

Do ponto de vista técnico, este desafio foi muito mais do que um exercício introdutório de ETL. Ele exigiu leitura crítica do problema, adaptação a mudanças externas e decisões arquiteturais conscientes — exatamente o tipo de cenário encontrado em ambientes profissionais.

Ao longo do processo, demonstrei:

- Capacidade de **analisar dependências quebradas** e propor alternativas viáveis;
- Entendimento prático de **ETL aplicado a dados reais**;
- Atualização tecnológica ao migrar para **APIs modernas de IA generativa**;
- Preocupação com **manutenibilidade, baixo acoplamento e observabilidade**;
- Autonomia para ir além do material base sem perder o objetivo pedagógico.

Para recrutadores e equipes técnicas, esse projeto evidencia não apenas conhecimento em Python e IA generativa, mas principalmente a habilidade de **resolver problemas em contextos imperfeitos**, algo fundamental em projetos de dados no mundo real.

Mais do que entregar um notebook funcional, o foco foi construir uma solução adaptável, sustentável e alinhada com boas práticas de engenharia.

Esse é o tipo de abordagem que levo para projetos profissionais: entender o problema, respeitar o contexto e entregar valor mesmo diante de limitações técnicas.

---

Agradeço ao Luiz F. P. Quirino (luizfpq) pela inspiração e código que serviu de ponto de partida e análise!

