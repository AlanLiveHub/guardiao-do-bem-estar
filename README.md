# Guardião do Bem-Estar 🌟 
### Seu Companheiro Digital para uma Vida Mais Leve e Feliz!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- Adicione outros badges se desejar, ex: status do build, versão do Python -->

<p align="center">
  <!-- Substitua pela URL da sua imagem de logo ou remova se não tiver -->
  <img src="URL_PARA_UM_LOGO_OU_IMAGEM_LEGAL_DO_PROJETO_SE_TIVER.png" alt="Guardião do Bem-Estar Logo" width="200"/>
</p>

**Este projeto é fruto da inspiradora Jornada da Imersão IA da Alura!** 🚀

Você já sentiu que precisava de um empurrãozinho para cultivar hábitos mais saudáveis ou de um ombro amigo digital nos momentos em que a energia está um pouco baixa? Apresentamos o **Guardião do Bem-Estar**, um chatbot inteligente e empático projetado para ser seu aliado na jornada por uma mente e corpo mais equilibrados!

Este projeto nasceu da crença de que pequenas ações positivas no dia a dia podem gerar grandes transformações. Queremos te ajudar a construir e manter hábitos que promovam o bem-estar físico e mental, oferecendo encorajamento, ferramentas simples e um espaço seguro para você se conectar consigo mesmo.

---

## 🎯 Sobre o Projeto

O "Guardião do Bem-Estar" é um chatbot inteligente e empático, atuando como um companheiro digital para auxiliar usuários a construir e manter hábitos que promovam o bem-estar físico e mental.
Este chatbot foi desenvolvido como um projeto prático durante a **Imersão IA da Alura**, com o objetivo de explorar o potencial da Inteligência Artificial Generativa (utilizando Google Gemini) para criar ferramentas que promovam o autocuidado e o bem-estar emocional, oferecendo encorajamento, direcionamento ético e um toque de gamificação para tornar a jornada mais leve.

---

## ✨ O que o Guardião já pode fazer por você?

Estamos construindo o Guardião passo a passo, e ele já aprendeu alguns truques incríveis para te apoiar:

*   **Mensagem de Boas-Vindas Automática:** Assim que você abre o chat, o Guardião te recebe com uma saudação e o importante disclaimer sobre ajuda profissional.
*   **Conversas Amigáveis e Empáticas:** Interaja com um chatbot que te ouve e responde com positividade, pronto para te acompanhar nas pequenas vitórias e desafios.
*   **Check-in Emocional Inteligente:**
    *   Como você está se sentindo hoje? Compartilhe em uma **escala numérica (1-5)** ou com uma **palavra** que descreva sua energia (o bot alterna a pergunta!).
    *   Com base na sua resposta, o Guardião oferece validação, **concede pontos de bem-estar** e sugere uma micro-ação ou exercício personalizado!
*   **Kit de Primeiros Socorros Emocionais (Funcionalidades Guiadas):**
    *   **Respiração Profunda:** Se precisar de um momento de calma, o Guardião te guia em um exercício de 3 respirações profundas.
    *   **Atenção aos Sons:** Um exercício de mindfulness guiado para te ajudar a focar no presente.
    *   **Escaneamento Corporal Curto:** Uma prática guiada para conectar-se com seu corpo e liberar tensões.
    *   **Técnica das "Três Coisas Boas":** O Guardião te incentiva a listar três coisas pelas quais você é grato, ajudando a cultivar uma perspectiva positiva.
*   **Gamificação Suave:**
    *   **Ganhe Pontos de Bem-Estar!** Receba pontos ao completar check-ins, iniciar exercícios guiados e listar suas três coisas boas. O Guardião te informa sobre seus ganhos e o total!
*   **Celebração de Pequenas Vitórias:** O Guardião reconhece e celebra quando você relata ter completado uma sugestão ou um micro-hábito!
*   **Sugestão de Micro-Hábitos:** Em momentos oportunos, o Guardião pode sugerir pequenas ações positivas para o seu dia.
*   **Interface Limpa e Acolhedora:** Um chat bonito e fácil de usar, com um fundo escuro projetado para transmitir tranquilidade e animações de digitação para uma interação mais dinâmica.
*   **Persistência da Conversa:** O Guardião se esforça para lembrar do contexto da sua conversa dentro da sessão atual (graças à persistência do histórico do SDK na sessão Flask).
*   **Sempre Alerta para sua Segurança (Nosso Compromisso Nº 1!):**
    *   **DISCLAIMER IMPORTANTE:** O Guardião é uma ferramenta de suporte e formação de hábitos. **ELE NÃO SUBSTITUI ACONSELHAMENTO MÉDICO, PSICOLÓGICO OU PSIQUIÁTRICO PROFISSIONAL.**
    *   Se você expressar sentimentos de desesperança intensa ou sofrimento agudo, o Guardião está programado para **interromper imediatamente** as sugestões de hábitos e te fornecer informações de contato para serviços de apoio profissional, como o **CVV (Centro de Valorização da Vida - Ligue 188 ou acesse cvv.org.br)**. Sua segurança e bem-estar são nossa prioridade máxima.

---

## 🚀 O Futuro é Brilhante: O que Vem por Aí!

A jornada do Guardião está só começando! Estamos animados com as próximas funcionalidades que irão turbinar seu bem-estar:

*   **Conexão Mente-Corpo Fortalecida:** Instruir o Guardião para sempre buscar conectar hábitos físicos com seus benefícios mentais de forma mais explícita.
*   **Gamificação Mais Elaborada:** Acompanhar "sequências" de dias mantendo um hábito, talvez pequenos emblemas ou reconhecimentos visuais.
*   **Base de Conhecimento Inteligente (RAG):**
    *   Inicialmente, usar RAG para fornecer os **scripts exatos dos exercícios guiados**, garantindo consistência e qualidade.
    *   Futuramente, expandir para informações sobre bem-estar e benefícios de hábitos.
*   **Lembretes Amigáveis (Reativo):** Permitir que o usuário peça ao Guardião para lembrá-lo de fazer uma pausa ou um micro-hábito.
*   **Refinamento Contínuo:** Melhorar os prompts, a naturalidade da conversa e a variedade de sugestões.

---

## 🛠️ Tecnologias Utilizadas

Este projeto está sendo construído com um mix de tecnologias modernas e poderosas:

*   **Backend:** Python com Flask (um microframework web leve e eficiente).
*   **Inteligência Artificial:** Google Gemini (especificamente o modelo `gemini-1.5-flash-latest`), uma LLM de ponta para conversas naturais, geração de sugestões e respostas empáticas.
*   **Frontend:** HTML, CSS (com foco em design responsivo, tema escuro para bem-estar e animações) e JavaScript puro para uma interface de chat interativa e dinâmica.
*   **Gerenciamento de Sessão e Persistência Inicial:** Flask sessions para manter o contexto da conversa do usuário (histórico da UI), estado da conversa (flags de check-in, ofertas de guia, etc.), o histórico da conversa do SDK Gemini e os pontos de gamificação.
*   **Estrutura do Projeto:** Organização modular no backend (separando configurações, lógica do chatbot, prompts, gerenciamento de sessão e utilitários) e no frontend (separando CSS e JavaScript em arquivos dedicados).
*   **Controle de Versão:** Git e GitHub, com um arquivo `.gitignore` para manter o repositório limpo.
*   **Ambiente:** Python, Gerenciamento de dependências com `pip` e `requirements.txt`, Variáveis de ambiente com `python-dotenv`.

**Planejado para o Futuro (Tecnologias):**
*   **Persistência de Dados Avançada:** Bancos de dados (como SQLite ou PostgreSQL) para gamificação de longo prazo e histórico de usuário persistente.
*   **RAG (Retrieval Augmented Generation):** Integração com um sistema de RAG.

---

## ⚙️ Como Rodar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git
    cd NOME_DO_SEU_REPOSITORIO
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    # No Windows: venv\Scripts\activate
    # No macOS/Linux: source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt 
    ```
    *(Certifique-se de que seu `requirements.txt` contém `Flask`, `google-generativeai`, `python-dotenv`)*

4.  **Configure suas variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz do projeto (no mesmo nível que `app.py`).
    *   Adicione sua chave da API Gemini:
        ```env
        GEMINI_API_KEY=SUA_CHAVE_API_AQUI
        ```

5.  **Execute o aplicativo Flask:**
    ```bash
    python3 app.py
    ```
6.  Abra seu navegador e acesse `http://127.0.0.1:5000/`.

---

## 💖 Junte-se a Nós Nesta Jornada!

O "Guardião do Bem-Estar" é mais que um chatbot; é um convite para você investir no seu bem mais precioso: você mesmo(a). Estamos empolgados para continuar desenvolvendo esta ferramenta e esperamos que ela possa trazer mais leveza, consciência e alegria para o seu dia a dia.

**Fique ligado para mais atualizações e sinta-se à vontade para experimentar o Guardião!**
*(Se o projeto estiver hospedado publicamente, adicione o link aqui. Ex: [Experimente o Guardião do Bem-Estar Aqui!](URL_DO_SEU_APP_HOSPEDADO))*

---
<!-- 
## 🤝 Como Contribuir (Opcional)

Adoramos contribuições! Se você tem ideias, sugestões ou quer ajudar no desenvolvimento, por favor:
1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaNovaFeature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona MinhaNovaFeature'`).
4. Faça push para a branch (`git push origin feature/MinhaNovaFeature`).
5. Abra um Pull Request.
-->