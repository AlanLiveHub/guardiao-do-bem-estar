# Guardião do Bem-Estar 🌟 
### Seu Companheiro Digital para uma Vida Mais Leve e Feliz!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <!-- Substitua pela URL da sua imagem ou remova se não tiver -->
  <img src="URL_PARA_UM_LOGO_OU_IMAGEM_LEGAL_DO_PROJETO_SE_TIVER.png" alt="Guardião do Bem-Estar Logo" width="200"/>
</p>

**Este projeto é fruto da inspiradora Jornada da Imersão IA da Alura!** 🚀

Você já sentiu que precisava de um empurrãozinho para cultivar hábitos mais saudáveis ou de um ombro amigo digital nos momentos em que a energia está um pouco baixa? Apresentamos o **Guardião do Bem-Estar**, um chatbot inteligente e empático projetado para ser seu aliado na jornada por uma mente e corpo mais equilibrados!

Este projeto nasceu da crença de que pequenas ações positivas no dia a dia podem gerar grandes transformações. Queremos te ajudar a construir e manter hábitos que promovam o bem-estar físico e mental, oferecendo encorajamento, ferramentas simples e um espaço seguro para você se conectar consigo mesmo.

---

## 🎯 Sobre o Projeto

O "Guardião do Bem-Estar" é um chatbot inteligente e empático, atuando como um companheiro digital para auxiliar usuários a construir e manter hábitos que promovam o bem-estar físico e mental.
Este chatbot foi desenvolvido como um projeto prático durante a **Imersão IA da Alura**, com o objetivo de explorar o potencial da Inteligência Artificial Generativa (utilizando Google Gemini) para criar ferramentas que promovam o autocuidado e o bem-estar emocional, oferecendo encorajamento e direcionamento ético.

---

## ✨ O que o Guardião já pode fazer por você?

Estamos construindo o Guardião passo a passo, e ele já aprendeu alguns truques incríveis para te apoiar:

*   **Conversas Amigáveis e Empáticas:** Interaja com um chatbot que te ouve e responde com positividade, pronto para te acompanhar nas pequenas vitórias e desafios.
*   **Check-in Emocional Inteligente:**
    *   Como você está se sentindo hoje? Compartilhe em uma **escala numérica (1-5)** ou com uma **palavra** que descreva sua energia (o bot alterna a pergunta!).
    *   Com base na sua resposta, o Guardião oferece validação e sugere uma micro-ação personalizada para te ajudar a se sentir melhor ou a manter o bom astral!
*   **Guia de Respiração Relaxante:** Sentindo a tensão aumentar? Se o Guardião sugerir e você aceitar, ele te guiará, passo a passo, em um exercício simples de **3 respirações profundas** para trazer calma e foco.
*   **Interface Limpa e Acolhedora:** Um chat bonito e fácil de usar para que sua experiência seja a mais agradável possível, com um fundo escuro projetado para transmitir tranquilidade.
*   **Persistência da Conversa:** O Guardião se esforça para lembrar do contexto da sua conversa dentro da sessão atual, mesmo se o servidor reiniciar (graças à persistência do histórico do SDK na sessão Flask).
*   **Sempre Alerta para sua Segurança (Nosso Compromisso Nº 1!):**
    *   **DISCLAIMER IMPORTANTE:** O Guardião é uma ferramenta de suporte e formação de hábitos. **ELE NÃO SUBSTITUI ACONSELHAMENTO MÉDICO, PSICOLÓGICO OU PSIQUIÁTRICO PROFISSIONAL.**
    *   Se você expressar sentimentos de desesperança intensa ou sofrimento agudo, o Guardião está programado para **interromper imediatamente** as sugestões de hábitos e te fornecer informações de contato para serviços de apoio profissional, como o **CVV (Centro de Valorização da Vida - Ligue 188 ou acesse cvv.org.br)**. Sua segurança e bem-estar são nossa prioridade máxima.

---

## 🚀 O Futuro é Brilhante: O que Vem por Aí!

A jornada do Guardião está só começando! Estamos animados com as próximas funcionalidades que irão turbinar seu bem-estar:

*   **Kit de Primeiros Socorros Emocionais Turbinado:** Mais exercícios guiados de respiração e mindfulness (como foco nos sons), além da inspiradora técnica das "Três Coisas Boas" para cultivar a gratidão.
*   **Formação de Micro-Hábitos Poderosos:** O Guardião vai te ajudar a incorporar pequenas ações positivas no seu dia e celebrar cada conquista com você!
*   **Conexão Mente-Corpo Fortalecida:** Entenda como cada hábito físico pode impulsionar sua clareza mental e energia emocional, com o Guardião fazendo essas conexões explicitamente.
*   **Gamificação Leve e Divertida:** Ganhe pontos por check-ins e por completar micro-hábitos, acompanhe "sequências" de dias mantendo um hábito. Cuidar de si mesmo pode ser uma aventura!
*   **Base de Conhecimento Inteligente (RAG):** O Guardião terá acesso a informações validadas sobre bem-estar, benefícios de hábitos e scripts de exercícios ainda mais detalhados para te oferecer um suporte cada vez mais rico e preciso.
*   **Lembretes Amigáveis:** Para aquelas pausas e momentos de autocuidado que a gente esquece na correria.

---

## 🛠️ Tecnologias Utilizadas

Este projeto está sendo construído com um mix de tecnologias modernas e poderosas:

*   **Backend:** Python com Flask (um microframework web leve e eficiente).
*   **Inteligência Artificial:** Google Gemini (especificamente o modelo `gemini-1.5-flash-latest`), uma LLM de ponta para conversas naturais, geração de sugestões e respostas empáticas.
*   **Frontend:** HTML, CSS (com foco em design responsivo e temas que promovem bem-estar) e JavaScript puro para uma interface de chat interativa e dinâmica.
*   **Gerenciamento de Sessão e Persistência Inicial:** Flask sessions para manter o contexto da conversa do usuário (histórico da UI), estado da conversa (flags de check-in, etc.) e o histórico da conversa do SDK Gemini (para continuidade).
*   **Estrutura do Projeto:** Organização modular no backend (separando configurações, lógica do chatbot, prompts, gerenciamento de sessão e utilitários) e no frontend (separando CSS e JavaScript).
*   **Controle de Versão:** Git e GitHub.
*   **Ambiente:** Python, Gerenciamento de dependências com `pip` e `requirements.txt`, Variáveis de ambiente com `python-dotenv`.

**Planejado para o Futuro:**
*   **Persistência de Dados Avançada:** Bancos de dados (como SQLite ou PostgreSQL) para funcionalidades mais complexas como gamificação de longo prazo e histórico de usuário persistente.
*   **RAG (Retrieval Augmented Generation):** Integração com um sistema de RAG para enriquecer as respostas do LLM.

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
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt 
    ```
    *(Certifique-se de ter um arquivo `requirements.txt` com `Flask`, `google-generativeai`, `python-dotenv` e `Werkzeug` – se não estiver usando a versão mais recente do Flask que já o inclui como dependência transitória para `flask run`)*

4.  **Configure suas variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz do projeto.
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
_(Se o projeto estiver hospedado publicamente, adicione o link aqui)_

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