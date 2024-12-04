# Projeto: Apigame

## **Descrição**
Desenvolvimento de um jogo web simples, chamado **Apigame**, integrado com pelo menos **duas APIs** para funcionalidades adicionais. O projeto será implementado com o framework Flask, terá suporte a multiusuários e será hospedado online para acesso remoto via navegador.

---

## **Fase 1: Planejamento (03/12)**

### **Definir o escopo do projeto**
- Criar um jogo simples com integração de APIs.
- Funcionalidade principal: Jogo **Pedra, Papel e Tesoura** com ranking global.

### **Requisitos técnicos**
- Suporte a **multiusuários** com conexões simultâneas (threads).
- Interface web amigável e acessível **remotamente** (não localhost).
- Código fonte **devidamente comentado** e funcional.

### **Entregáveis**
1. **Código Fonte**:
   - Bem estruturado e comentado.
2. **Relatório em PDF**, incluindo:
   - Identificação do projeto.
   - Justificativa e escolha do framework.
   - Arquitetura do sistema.
   - APIs usadas e detalhes de integração.
   - Dificuldades enfrentadas e conclusões.
3. **Apresentação**:
   - Explicação do código.
   - Demonstração funcional da aplicação.

---

## **Fase 2: Configuração Inicial (03/12 - 04/12)**

### **Instalar e configurar o ambiente de desenvolvimento**
- Instalar Flask e extensões, como `Flask-Cors`.
- Configurar repositório Git para versionamento.
- Criar a estrutura inicial do projeto.

### **Estrutura básica do projeto**
apigame/
├── static/
├── templates/
├── app.py
├── api/
├── requirements.txt
├── README.md


### **Funcionalidades iniciais**
- Criar rota básica (`/`) para exibir a página inicial.
- Configurar threading no Flask para suporte a múltiplos usuários.

---

## **Fase 3: Desenvolvimento (05/12 - 06/12)**

### **Backend (Flask)**
#### **Endpoints obrigatórios**
- `/play`: Jogar contra a máquina ou outro usuário.
- `/ranking`: Exibir o ranking global.
- `/share`: Gerar links para desafios.

#### **Integração de APIs**
- **API 1**: *PositionStack* ou *IP Geolocation*
  - Utilizar para identificar a localização dos jogadores.
- **API 2**: *OpenWeatherMap*
  - Customizar o tema do jogo baseado nas condições climáticas.

#### **Banco de Dados**
- Utilizar SQLite para armazenar:
  - Usuários.
  - Pontuações e rankings.

### **Frontend (HTML/CSS/JS)**
#### **Criação da interface**
- Página inicial com:
  - Botão para iniciar o jogo.
  - Visualização do ranking global.
  - Geração de links para desafios.

#### **Estilização**
- Utilizar CSS ou frameworks como Bootstrap.

#### **Integração**
- Fazer chamadas aos endpoints usando **AJAX** ou **Fetch API** no JavaScript.

---

## **Fase 4: Hospedagem (06/12)**

### **Configurar o serviço de hospedagem**
- **Opções recomendadas**:
  - PythonAnywhere.
  - Render.
  - Heroku.

### **Testar a aplicação**
- Validar o funcionamento do sistema remotamente, garantindo:
  - Acessibilidade online.
  - Funcionalidade de todas as rotas.

---

## **Fase 5: Finalização e Documentação (07/12 - 08/12)**

### **Preparar a apresentação**
- Gravar um vídeo ou criar slides explicando:
  - Estrutura do código.
  - Funcionalidades implementadas.
  - Exemplos de uso da aplicação.

### **Escrever o relatório**
1. **Identificação**:
   - Nome do projeto, autores e objetivo.
2. **Justificativa**:
   - Motivos para escolha do Flask como framework.
3. **Arquitetura do Sistema**:
   - Diagrama e descrição das camadas.
4. **APIs Integradas**:
   - Detalhes sobre a utilização de PositionStack e OpenWeatherMap.
5. **Dificuldades e Conclusão**:
   - Desafios enfrentados durante o desenvolvimento.
   - Resultados alcançados.

### **Empacotamento e revisão**
- Compactar:
  - Código-fonte.
  - Relatório em PDF.
- Validar novamente a aplicação antes da entrega.

### **Entrega**
- Submissão no AVA até **08/12/2024, 23:55**.

---

## **Checklist para Controle do Progresso**

| Tarefa                            | Status      | Prazo  |
|-----------------------------------|-------------|--------|
| Definir escopo e APIs             | 🔲 Pendente | 03/12  |
| Estruturar projeto inicial        | 🔲 Pendente | 04/12  |
| Implementar backend Flask         | 🔲 Pendente | 05/12  |
| Desenvolver frontend (UI)         | 🔲 Pendente | 05/12  |
| Integrar APIs externas            | 🔲 Pendente | 06/12  |
| Hospedar aplicação online         | 🔲 Pendente | 06/12  |
| Preparar apresentação e relatório | 🔲 Pendente | 07/12  |
| Submeter trabalho final           | 🔲 Pendente | 08/12  |
