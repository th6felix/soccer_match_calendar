<div align="center">
  <h1 align="center"> Calendário dos jogos de futebol </h1>
  <p> Automação para coletar dados sobre jogos de futebol em site esportivo, tratar essas informações e adicionar aos eventos do Google Calendar. </p>
  <br>
</div>


## ⚙️ Como Funciona
Essa automação realiza os seguintes passos:

1. **Coleta de dados**  
   - Coleta das informações de jogos de futebol no site [Globo Esporte](https://globoesporte.globo.com) para qualquer time durante o ano, com a capacidade de personalizar a busca por diferentes times.
     
     #### Tecnologia: Web Scraping (Requests)
  
2. **Tratamento dos Dados**  
   - Conversão das datas e horários dos jogos para o formato desejado.
   - Filtro dos jogos do dia.
     
      #### Tecnologia: Pandas
    
3. **Integração com a API**  
   - Configuração dos dados de acesso à api.
   - Criação e atualização dos eventos no Google Calendar com os jogos coletados.
     
     #### Tecnologia: Google Calendar API

4. **Execução Automática**  
   - O script é configurado para rodar automaticamente após 45 minutos quando o PC for ligado
   
     #### Tecnologia: Task Scheduler do Windows

<br>

## 🛠️ Como Configurar e Adaptar

1. **Instalar as Dependências**  
   ```bash
   pip install beautifulsoup4 requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas

2. **Configurar a Conta de Serviço do Google**
    - Crie uma conta de serviço no Google Cloud Console.
    - Baixe as credenciais da conta de serviço e coloque o arquivo JSON na pasta do projeto.
    - Dê permissões à conta de serviço para adicionar eventos ao seu calendário.

3. **Alterar o Código para Seu Time**
    - BR: alterar time na url do site fonte
    - demais: ajustar url e lógica de tratamento

4. **Configuração do Agendador de Tarefas (Windows)**
    - Abra o "Agendador de Tarefas" no Windows.
    - Crie uma nova tarefa para rodar o script Python automaticamente
    - Configurar "disparadores".

