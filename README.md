# Meu Guardião do Bem-Estar 🌟 – Seu Companheiro Digital para uma Vida Mais Leve e Feliz!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <!-- Substitua pela URL da sua imagem ou remova se não tiver -->
  <img src="URL_PARA_UM_LOGO_OU_IMAGEM_LEGAL_DO_PROJETO_SE_TIVER.png" alt="Meu Guardião do Bem-Estar Logo" width="200"/>
</p>

Você já sentiu que precisava de um empurrãozinho para cultivar hábitos mais saudáveis ou de um ombro amigo digital nos momentos em que a energia está um pouco baixa? Apresentamos o **Meu Guardião do Bem-Estar**, um chatbot inteligente e empático projetado para ser seu aliado na jornada por uma mente e corpo mais equilibrados!

Este projeto nasceu da crença de que pequenas ações positivas no dia a dia podem gerar grandes transformações. Queremos te ajudar a construir e manter hábitos que promovam o bem-estar físico e mental, oferecendo encorajamento, ferramentas simples e um espaço seguro para você se conectar consigo mesmo.

---

## ✨ O que o Guardião já pode fazer por você?

Estamos construindo o Guardião passo a passo, e ele já aprendeu alguns truques incríveis para te apoiar:

*   **Conversas Amigáveis e Empáticas:** Interaja com um chatbot que te ouve e responde com positividade, pronto para te acompanhar nas pequenas vitórias e desafios.
*   **Check-in Emocional Inteligente:**
    *   Como você está se sentindo hoje? Compartilhe em uma **escala numérica (1-5)** ou com uma **palavra** que descreva sua energia.
    *   Com base na sua resposta, o Guardião oferece validação e sugere uma micro-ação personalizada para te ajudar a se sentir melhor ou a manter o bom astral!
*   **Guia de Respiração Relaxante:** Sentindo a tensão aumentar? Peça ajuda e o Guardião te guiará, passo a passo, em um exercício simples de **3 respirações profundas** para trazer calma e foco imediatos.
*   **Interface Limpa e Acolhedora:** Um chat bonito e fácil de usar para que sua experiência seja a mais agradável possível.
*   **Sempre Alerta para sua Segurança (Nosso Compromisso Nº 1!):**
    *   **DISCLAIMER IMPORTANTE:** O Guardião é uma ferramenta de suporte e formação de hábitos. **ELE NÃO SUBSTITUI ACONSELHAMENTO MÉDICO, PSICOLÓGICO OU PSIQUIÁTRICO PROFISSIONAL.**
    *   Se você expressar sentimentos de desesperança intensa ou sofrimento agudo, o Guardião está programado para **interromper imediatamente** as sugestões de hábitos e te fornecer informações de contato para serviços de apoio profissional, como o **CVV (Centro de Valorização da Vida - Ligue 188 ou acesse cvv.org.br)**. Sua segurança e bem-estar são nossa prioridade máxima.

---

## 🚀 O Futuro é Brilhante: O que Vem por Aí!

A jornada do Guardião está só começando! Estamos animados com as próximas funcionalidades que irão turbinar seu bem-estar:

*   **Kit de Primeiros Socorros Emocionais Turbinado:** Mais exercícios guiados de respiração e mindfulness, além da inspiradora técnica das "Três Coisas Boas" para cultivar a gratidão.
*   **Formação de Micro-Hábitos Poderosos:** Vamos te ajudar a incorporar pequenas ações positivas no seu dia (beber mais água, fazer uma pausa, arrumar a cama) e celebrar cada conquista com você!
*   **Conexão Mente-Corpo Fortalecida:** Entenda como cada hábito físico pode impulsionar sua clareza mental e energia emocional.
*   **Gamificação Leve e Divertida:** Ganhe pontos, desbloqueie "conquistas" por manter seus hábitos e check-ins em dia. Cuidar de si mesmo pode ser uma aventura!
*   **Base de Conhecimento Inteligente (RAG):** O Guardião terá acesso a informações validadas sobre bem-estar, benefícios de hábitos e scripts de exercícios ainda mais detalhados para te oferecer um suporte cada vez mais rico.
*   **Lembretes Amigáveis:** Para aquelas pausas e momentos de autocuidado que a gente esquece na correria.

---

## 🛠️ Tecnologias Utilizadas

Este projeto está sendo construído com um mix de tecnologias modernas e poderosas:

*   **Backend:** Python com Flask (um microframework web leve e eficiente).
*   **Inteligência Artificial:** Google Gemini (especificamente o modelo `gemini-1.5-flash-latest`), uma LLM de ponta para conversas naturais, geração de sugestões e respostas empáticas.
*   **Frontend:** HTML, CSS e JavaScript puro para uma interface de chat interativa e responsiva.
*   **Gerenciamento de Sessão:** Flask sessions para manter o contexto da conversa e o progresso do usuário.
*   **Persistência de Dados:**
    *   Uso de `session` do Flask para armazenar o histórico da conversa do SDK Gemini e o estado da UI.
    *   *(Planejado):* Bancos de dados (como SQLite ou outros) para funcionalidades mais complexas como gamificação e histórico de longo prazo.
*   **Hospedagem (Exemplo/Planejado):** _(Opcional: Mencione se já tiver um plano ou onde está hospedado, ex: PythonAnywhere, Google Cloud Run, Heroku, etc.)_
*   **RAG (Planejado):** Integração com um sistema de Retrieval Augmented Generation para enriquecer as respostas do LLM com informações de um banco de dados de conhecimento específico.

---

## ⚙️ Como Rodar Localmente (Exemplo)

_(Esta seção é um exemplo. Adapte conforme sua estrutura de projeto e dependências.)_

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
    cd NOME_DO_REPOSITORIO
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    # venv\Scripts\activate
    # No macOS/Linux:
    # source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt 
    ```
    *(Certifique-se de ter um arquivo `requirements.txt` com `Flask`, `google-generativeai`, `python-dotenv`, etc.)*

4.  **Configure suas variáveis de ambiente:**
    *   Crie um arquivo `.env` na raiz do projeto.
    *   Adicione sua chave da API Gemini:
        ```env
        GEMINI_API_KEY=SUA_CHAVE_API_AQUI
        ```

5.  **Execute o aplicativo Flask:**
    ```bash
    python app.py
    ```
6.  Abra seu navegador e acesse `http://127.0.0.1:5000/`.

---

## 💖 Junte-se a Nós Nesta Jornada!

O "Meu Guardião do Bem-Estar" é mais que um chatbot; é um convite para você investir no seu bem mais precioso: você mesmo(a). Estamos empolgados para continuar desenvolvendo esta ferramenta e esperamos que ela possa trazer mais leveza, consciência e alegria para o seu dia a dia.

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