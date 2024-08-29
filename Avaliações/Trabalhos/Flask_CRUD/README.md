# Cloud-Verse (logo)

1. **Arquivo base.html**
    - É nosso arquivo base onde contém todas as partes fixas do nosso site, um cabeçalho, um body e uma barra de navegação, além do script.js para as animações como as particulas de fundo e o menu dropdown

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="pt-br">
  <head>
    <meta charset="UTF-8">
    <title>Cloud Verse</title>
    <!--inclui arquivo css do bootstrap -->
    <!--inclui arquivo css pra icones do unicons a partir de uma url -->
    <!--inclui versão externa do css do bootstrap a partir de uma cdn -->
    <!--inclui arquivo css personalizado localizado na pasta do projeto -->
    <!-- Define as configurações de viewport para dispositivos móveis, ajustando a escala e o tamanho do conteúdo para se ajustar à tela -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="https://unicons.iconscout.com/release/v2.1.9/css/unicons.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  </head>
  <body>
  <!-- fixa o conteúdo no topo da página durante o rolar -->
    <div class="sticky-top">
    <!-- Define uma barra de navegação com a classe navbar e um fundo escuro. O atributo data-bs-theme="dark" aplica um tema escuro para a barra de navegação. -->
      <nav class="navbar bg-dark border-bottom border-bottom-dark" data-bs-theme="dark">
      <!-- Conteiner para a logo da pagina -->
        <div class="logo_name_container">
        <!-- imagem da logo com a fonte definida com uma classe (logo_com_nome) pra estilização -->
          <img src="{{ url_for('static', filename='img/logo_com_nome1.png') }}" alt="Cloud Verse Logo" class="logo_com_nome">
        </div>
        <!-- cria um grupo de botoes adicional pro dropdown do usuario -->
        <div class="btn-group">
          {% if 'username' in session: %}
            <div class="btn-group">
              <!-- adiciona um manipulador de eventos Js para chamar a função toggleDropdown() quando clicado-->
              <!-- classe btn-usuario pra estilizar -->
              <button class ="btn-usuario" onclick="toggleDropdown()">{{ session['username'] }}</button>
              <!-- define o menu suspenso que aparece quando o botao é clicado -->
              <div class="dropdown-menu">
              <!-- link pra página de perfil (ainda nao tem) -->
                <a href="#">Perfil</a>
                <!-- link pra ação de logout com o destino -->
                <a href="{{ url_for('default.logout') }}">Sair</a>
              </div>              
            </div>
            <!-- Finaliza a verificação condicional pra autenticação do user-->
          {% endif %}
        </div>
      </nav>
    </div>
    <!-- Inicia a div com a class container, usada para centralizar e adicionar espaçamento ao conteúdo -->
    <div class="container">
    <!-- cria um elemento canvas com id rainfall pra animação de chuva, classe 'stars' pra estilização.  -->
      <canvas id="rainfall" class="stars"></canvas>
      <!-- Inicia a div 'extended-content' que vai ser preenchida com o conteúdo específico das páginas -->
      <div class="extended-content">
      <!-- Define um bloco de conteúdo onde o conteúdo específico de cada página vai ser inserido -->
        {% block content %}
        <!-- Finaliza o bloco de donteúdo -->
        {% endblock %}
      </div>
    </div>
```
## Script.js para a função rain

```JavaScript
    <script>
        // Obtém o elemento canvas e seu contexto de renderização 2D
        const canvas = document.getElementById('rainfall');
        const ctx = canvas.getContext('2d');

        // Define o tamanho do canvas para coincidir com o tamanho da janela
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Array pra armazenar as gotas de chuva
        const raindrops = [];

        // Função pra criar uma nova gota de chuva 
        function createRaindrop() {
            // Gera posições aleatórias pra gota de chuva
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            // Gera uma velocidade aleatória pra gota de chuva
            var velocity = Math.random() * 0.7 + 0.3;
            // Define a velocidade e direção da gota de chuva
            const speed = [[velocity, 0], [-velocity, 0]][Math.floor(Math.random() * 2)];

            //Define o comprimento e a cor da gota de chuva
            const length = 4;
            const color = ["#160518","#040125","#000f0e","#3b3544","#32293f","#5b457a","#120820","#242241","#2a574c","#2a3a57","#000000","#130022"][Math.floor(Math.random() * 13)];

            // Adiciona a nova gota de chuva ao array
            raindrops.push({ x, y, speed, length, color });
        }

        // Função pra atualizar as posições das gotas de chuva
        function updateRaindrops() {

            // Itera sobre cada gota de chuva
            for (let i = 0; i < raindrops.length; i++) {
                const raindrop = raindrops[i];

                // Atualiza a posição da gota de chuva com base na velocidade
                raindrop.y += raindrop.speed[0];
                raindrop.x += raindrop.speed[1];

                // Remove gotas de chuva que saíram da tela
                if (raindrop.y > canvas.height) {
                    raindrops.splice(i, 1); // Remove a gota do array
                    i--; // Ajusta o índice após a remoção
                }
            }
        }

        // Função pra desenhar as gotas de chuva no canvas
        function drawRaindrops() {

            // Limpa o canvas pra desenhar o próximo frame
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Itera sobre cada gota de chuva
            for (let i = 0; i < raindrops.length; i++) {
              const raindrop = raindrops[i];

              // Define a cor da gota de chuva
              ctx.strokeStyle = raindrop.color;
              ctx.lineWidth = 4;
              ctx.beginPath();

              // Desenha a gota de chuva como uma linha vertical
              ctx.moveTo(raindrop.x, raindrop.y);
              ctx.lineTo(raindrop.x, raindrop.y + raindrop.length);
              ctx.stroke();
            }
        }

        // Função pra animar as gotas de chuva
        function animate() {
            createRaindrop(); // Cria novas gotas
            updateRaindrops(); // Atualiza a posição das gotas
            drawRaindrops(); // Desenha as gotas de chuva
            requestAnimationFrame(animate); // Solicita o próximo frame de animação
        }

        // Inicia a animação
        animate();
    </script>
```
## Script.js para a função menu dropdown

```JavaScript
    <script>
    // Função pra alternar a visibilidade do menu dropdown
      function toggleDropdown() {
        const dropdownMenu = document.querySelector('.dropdown-menu');

        // Alterna a exibição entre 'block' e 'none'
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
      }
    
      // Adiciona um evento de clique no documento
      document.addEventListener('click', function(event) {
        const button = document.querySelector('.btn-usuario');
        const dropdownMenu = document.querySelector('.dropdown-menu');

        // Fechar o dropdown se clicar fora do botão ou fora do menu
        if (!button.contains(event.target) && !dropdownMenu.contains(event.target)) {
          dropdownMenu.style.display = 'none';
        }
      });
    </script>
  </body>
</html>
```


```html 
<!-- index.html -->

<!-- Extende o template 'base.html', permitindo que herde a estrutura e os estilos definidos no template base -->
{% extends 'base.html' %}

<!-- Inicia o bloco de conteúdo onde o conteúdo específico desta página será inserido -->
{% block content %}

<!-- Inicia a div com a classe 'section', usada pra estilizar e organizar a seção de conteúdo -->
<div class="section">

    <!-- Inicia a div com a classe 'container', que centraliza o conteúdo e adiciona espaçamento -->
    <div class="container">
    
        <!-- Inicia a div com a classe 'row' para criar uma linha de grid. A classe 'full-height' faz com que a linha ocupe toda a altura disponível, e 'justify-content-center' centraliza o conteúdo horizontalmente -->
        <div class="row full-height justify-content-center">

        <!-- Inicia a div com a classe 'col-12', que ocupa toda a largura disponível na linha -->
        <!-- As classes 'text-center' e 'align-self-center' centralizam o texto e o conteúdo verticalmente --> 
        <!-- A classe 'py-5' adiciona padding (distancia entre o conteúdo e a borda)vertical -->
            <div class="col-12 text-center align-self-center py-5">

                <!-- Inicia uma div com a classe 'section', que aplica padding ao topo e ao fundo do elemento. A classe 'text-center' centraliza o texto -->
                <div class="section pb-5 pt-5 pt-sm-2 text-center">
                
                    <!-- Cria um cabeçalho de nível 6 com a classe 'mb-0' para margem inferior zero e 'pb-3' para padding inferior. Os spans contêm os textos "Entrar" e "Registrar-se" -->
                    <h6 class="mb-0 pb-3"><span>Entrar </span><span>Registrar-se</span></h6>
                    
                    <!-- Cria uma caixa de seleção (checkbox) com a classe 'checkbox'. O id e o name são definidos como 'reg-log' -->
                    <input class="checkbox" type="checkbox" id="reg-log" name="reg-log"/>
                    
                    <!-- Cria um rótulo (label) associado à caixa de seleção com o id 'reg-log'. Este rótulo pode ser estilizado ou usado para criar interatividade -->
                    <label for="reg-log"></label>
                    
                    <!-- Inicia a div com a classe 'card-3d-wrap', que aplica um efeito 3D no cartão. A classe 'mx-auto' centraliza horizontalmente o cartão -->
                    <div class="card-3d-wrap mx-auto">
                    
                        <!-- Inicia a div com a classe 'card-3d-wrapper', que é usada para envolver o cartão e aplicar os efeitos 3D -->
                        <div class="card-3d-wrapper">
                       
                            <!-- Inicia a parte frontal do cartão com a classe 'card-front' -->
                            <div class="card-front">
                            
                                <!-- Inicia a div com a classe 'center-wrap', que centraliza o conteúdo dentro do cartão frontal -->
                                <div class="center-wrap">
                                
                                    <!-- Inicia a div com a classe 'section' e 'text-center' para aplicar estilo e centralizar o texto -->
                                    <div class="section text-center">
                                    
                                        <!-- Inicia um formulário com o id 'loginForm', método POST e ação para enviar os dados para a raiz do site ('/') -->
                                        <form id="loginForm" method="POST" action="/">                                    
                                            <!-- Cria um cabeçalho de nível 4 com a classe 'mb-4' para margem inferior e 'pb-3' para padding inferior, com o texto "Entrar" -->
                                            <h4 class="mb-4 pb-3">Entrar</h4>
                                            
                                            <!-- Verifica se existe uma variável 'error' para mostrar mensagens de erro. -->
                                            {% if error %}
                                            
                                                <!-- Verifica se o primeiro item do array 'error' é 'login' -->
                                                {% if error[0] == 'login': %}                              
                                               
                                                    <!-- Exibe a mensagem de erro associada ao login, com a classe 'error' para estilização -->
                                                    <p class="error">{{ error[1] }}</p> 
                                                 
                                                {% endif %}
                                            {% endif %}

                                            <!-- Inicia uma div com a classe 'form-group' para agrupar os campos do formulário -->
                                            <div class="form-group">                                           
                                                <!-- Cria um campo de entrada de texto com a classe 'form-style', um texto de placeholder "Nome de usuário", e o id e name definidos como 'username'. O atributo 'required' indica que o campo deve ser preenchido -->
                                                <input type="text" class="form-style" placeholder="Nome de usuário" id="username" name="username" required>

                                                <!-- Adiciona um ícone ao lado do campo de entrada, usando as classes 'input-icon' e 'uil uil-user' -->
                                                <i class="input-icon uil uil-user"></i>
                                            </div>  

                                            <!-- Inicia a div com a classe 'form-group' e 'mt-2' para adicionar margem superior ao campo de senha -->
                                            <div class="form-group mt-2">                                          
                                                <!-- Cria um campo de entrada de senha com a classe 'form-style', um texto de placeholder "Senha", e o id e name definidos como 'password'. O atributo 'required' indica que o campo deve ser preenchido -->
                                                <input type="password" class="form-style" placeholder="Senha" id="password" name="password" required>

                                                <!-- Adiciona um ícone ao lado do campo de senha, usando as classes 'input-icon' e 'uil uil-lock-alt' -->
                                                <i class="input-icon uil uil-lock-alt"></i>
                                            </div>

                                            <!-- Inicia uma div com a classe 'remeber-forgot', usada para agrupar a caixa de seleção "Lembrar-me" e o link de "Esqueceu sua senha?" -->
                                            <div class="remeber-forgot">                                         
                                              <!-- Inicia um rótulo com a classe 'custom-checkbox' para estilizar a caixa de seleção -->
                                              <label class="custom-checkbox">
                                              
                                                <!-- Cria uma caixa de seleção (checkbox) com o id e o name definidos como 'lembrar-me' -->
                                                <input type="checkbox" id="lembrar-me" name="lembrar-me">
                                                
                                                <!-- Adiciona um elemento 'span' com a classe 'checkmark' para estilizar a caixa de seleção e o texto "Lembrar-me" -->
                                                <span class="checkmark"></span> Lembrar-me
                                              </label>        
                                            </div>

                                            <!-- Cria um botão de envio com a classe 'btn' e 'mt-4' para adicionar margem superior. O texto do botão é "Entrar" -->
                                            <button type="submit" class="btn mt-4">Entrar</button>
                                            
                                            <!-- Adiciona um parágrafo vazio para espaçamento e um link "Esqueceu sua senha?" com href="#" -->
                                            <p class="mb-0 mt-4 text-center"></p> <a href="#">Esqueceu sua senha?</a>
                                        </form>
                                    </div> <!-- Fecha a div 'section' que contém o formulário de login -->
                                </div> <!-- Fecha a div 'center-wrap' que centraliza o formulário no cartão frontal -->
                            </div> <!-- Fecha a div 'card-front' que representa a frente do cartão -->
                            
                            <!-- Inicia a parte traseira do cartão com a classe 'card-back' -->
                            <div class="card-back">

                                <!-- Inicia uma div com a classe 'center-wrap' para centralizar o conteúdo dentro do cartão traseiro -->
                                <div class="center-wrap">
                               
                                    <!-- Inicia uma div com a classe 'section' e 'text-center' para aplicar estilo e centralizar o texto -->
                                    <div class="section text-center">                                   
                                        <!-- Inicia um formulário com o id 'registerForm', método POST e ação para enviar os dados para a raiz do site ('/') -->
                                        <form id="registerForm" method="POST" action="/">                                     
                                            <!-- Cria um cabeçalho de nível 4 com a classe 'mb-3' para margem inferior e 'pb-3' para padding inferior, com o texto "Registrar-se" -->
                                            <h4 class="mb-3 pb-3">Registrar-se</h4>
                                            
                                            <!-- Verifica se existe uma variável 'error' para mostrar mensagens de erro -->
                                            {% if error %}
                                            
                                                <!-- Verifica se o primeiro item do array 'error' é 'register' -->
                                                {% if error[0] == 'register': %}
                                                
                                                    <!-- Exibe a mensagem de erro associada ao registro, com a classe 'error' para estilização -->
                                                    <p class="error">{{ error[1] }}</p>                                             
                                                {% endif %}
                                            {% endif %}

                                            <!-- Inicia a div com a classe 'form-group' para agrupar os campos do formulário -->
                                            <div class="form-group">                                         
                                                <!-- Cria um campo de entrada de texto com a classe 'form-style', um texto de placeholder "Nome Completo", e o id e name definidos como 'fullname'. O atributo 'required' pra ser preenchido -->
                                                <input type="text" class="form-style" placeholder="Nome Completo" id="fullname" name="fullname" required>

                                                <!-- Adiciona um ícone ao lado do campo de entrada, usando as classes 'input-icon' e 'uil uil-user' -->
                                                <i class="input-icon uil uil-user"></i>
                                            </div>  

                                            <!-- Inicia a div com a classe 'form-group' e 'mt-2' para adicionar margem superior ao campo de nome de usuário -->
                                            <div class="form-group mt-2">                                         
                                                <!-- Cria um campo de entrada de texto com a classe 'form-style', um texto de placeholder "Nome de usuário", o id e name definidos como 'username'. O atributo 'required' pra ser preenchido -->
                                                <input type="text" class="form-style" placeholder="Nome de usuário" id="username" name="username" required>

                                                <!-- Adiciona um ícone ao lado do campo de nome de usuário, usando as classes 'input-icon' e 'fas fa-hashtag' -->
                                                <i class="input-icon fas fa-hashtag"></i>
                                            </div> 

                                            <!-- Inicia a div com a classe 'form-group' e 'mt-2' para adicionar margem superior ao campo de e-mail -->
                                            <div class="form-group mt-2">                                           
                                                <!-- Cria um campo de entrada de e-mail com a classe 'form-style', um texto de placeholder "E-mail", e o id e name definidos como 'email'. O atributo 'required' pra ser preenchido -->
                                                <input type="email" class="form-style" placeholder="E-mail" id="email" name="email" required>

                                                <!-- Adiciona um ícone ao lado do campo de e-mail, usando as classes 'input-icon' e 'uil uil-at' -->
                                                <i class="input-icon uil uil-at"></i>
                                            </div>

                                            <!-- Inicia a div com a classe 'form-group' e 'mt-2' para adicionar margem superior ao campo de senha -->
                                            <div class="form-group mt-2">                                           
                                                <!-- Cria um campo de entrada de senha com a classe 'form-style', um texto de placeholder "Senha", e o id e name definidos como 'password'. O atributo 'required' pra ser preenchido -->
                                                <input type="password" class="form-style" placeholder="Senha" id="password" name="password" required>

                                                <!-- Adiciona um ícone ao lado do campo de senha, usando as classes 'input-icon' e 'uil uil-lock-alt' -->
                                                <i class="input-icon uil uil-lock-alt"></i>
                                            </div>

                                            <button href="" class="btn mt-4" type="submit">Registrar</button>
                                            <!-- Cria um botão de envio com a classe 'btn' e 'mt-4' para adicionar margem superior. O texto do botão é "Registrar" -->
                                        </form>
                                    </div> <!-- Fecha a div 'section' que contém o formulário de registro -->
                                </div> <!-- Fecha a div 'center-wrap' que centraliza o formulário no cartão traseiro -->
                            </div> <!-- Fecha a div 'card-back' que representa a parte traseira do cartão -->
                        </div> <!-- Fecha a div 'card-3d-wrapper' que envolve o cartão -->
                    </div> <!-- Fecha a div 'card-3d-wrap' que aplica o efeito 3D ao cartão -->
                </div> <!-- Fecha a div 'section' que envolve a área de conteúdo principal -->
            </div> <!-- Fecha a div 'col-12' que ocupa toda a largura da linha -->
        </div> <!-- Fecha a div 'row' que organiza as colunas -->
    </div> <!-- Fecha a div 'container' que centraliza o conteúdo -->
</div> <!-- Fecha a div 'section' que organiza a seção de conteúdo -->
{% endblock %} <!-- Fecha o bloco de conteúdo definido no início. -->
{% endblock %}
```


```html 
<!-- service_register-->
<!-- Estende o template 'base.html', incluindo o conteúdo deste arquivo dentro do bloco 'content' definido no template base -->
{% extends 'base.html' %}

<!-- Inicia o bloco 'content', onde será inserido o conteúdo específico desta página -->
{% block content %}

<!-- Cria a div com a classe 'master' para agrupar todo o conteúdo da página -->
<div class="master">

    <!-- Cria a div com a classe 'plan' que estiliza a seção principal do formulário -->
    <div class="plan">
        
        <!-- Cria a div com a classe 'inner' que contém o texto informativo e o formulário -->
        <div class="inner">
            
            <!-- Parágrafo com uma mensagem informativa para o usuário -->
            <p class="info">Atualmente você não possui serviços cadastrados. Deseja adicionar um serviço?</p>
            
            <!-- Início de um formulário com o id 'register_service_Form'. O método é POST, e o formulário envia dados para a rota '/user/add_service' -->
            <form id="register_service_Form" method="POST" action="/user/add_service">
                
                <!-- Inicia uma lista não ordenada (ul) com a classe 'features', provavelmente usada para estilizar os itens da lista -->
                <ul class="features">
                    
                    <!-- Título para o formulário com margens aplicadas, indicando a seção de registro -->
                    <h4 class="mb-3 pb-3">Registrar-se</h4>
                    
                    <!-- Verifica se existe alguma variável de erro disponível -->
                    {% if error %}
        
                        <!-- Se o primeiro item da lista de erros for 'register', exibe a mensagem de erro correspondente -->
                        {% if error[0] == 'register': %}
                            
                            <!-- Parágrafo que exibe a mensagem de erro, estilizada com a classe 'error' -->
                            <li>
                                <p class="error">{{ error[1] }}</p> 
                            </li>
                        {% endif %}
                    {% endif %}
                    <li>
                        <!-- Inicia a div com a classe 'form-group' para agrupar o campo de entrada de nome da aplicação -->
                        <div class="form-group">
                            
                            <!-- Campo de entrada de texto para o nome da aplicação, com a classe 'form-style' para estilização. O campo é obrigatório -->
                            <input type="text" class="form-style" placeholder="Nome da aplicação" id="service_name" name="service_name" required>
                            
                            <!-- Ícone ao lado do campo de texto, estilizado com as classes 'input-icon' e 'uil uil-user' -->
                            <i class="input-icon uil uil-user"></i>
                        </div>
                    </li>
                    <li>
                        <!-- Cria um rótulo com a classe 'cyberpunk-checkbox-label' para estilizar o checkbox e o texto associado -->
                        <label class="cyberpunk-checkbox-label">                        
                            <!-- Checkbox para a opção 'Website', com a classe 'cyberpunk-checkbox' para estilização -->
                            <input type="checkbox" class="cyberpunk-checkbox" id="app_web" name="app_web">
                         
                            <!-- Texto associado ao checkbox, indicando a opção 'Website' -->
                            <span><strong>Website </strong></span>(html/css/js)
                        </label>
                    </li>
                    <li>
                        <!-- Rótulo estilizado para o checkbox da opção 'Aplicativo (Android)' -->
                        <label class="cyberpunk-checkbox-label">
                            
                            <!-- Checkbox para a opção 'Aplicativo (Android)' -->
                            <input type="checkbox" class="cyberpunk-checkbox" id="app_android" name="app_android">
            
                            <!-- Texto associado ao checkbox, indicando a opção 'Aplicativo (Android)' -->
                            <span><strong>Aplicativo </strong>(Android)</span>                       
                        </label>
                    </li>

                    <li> 
                        <!-- Rótulo estilizado para o checkbox da opção 'Aplicativo (IOS)' -->
                        <label class="cyberpunk-checkbox-label">
                           
                            <!-- Checkbox para a opção 'Aplicativo (IOS)' -->
                            <input type="checkbox" class="cyberpunk-checkbox" id="app_IOS" name="app_IOS">

                            <span><strong>Aplicativo </strong>(IOS)</span>
                            <!-- Texto associado ao checkbox, indicando a opção 'Aplicativo (IOS)' -->
                        </label>
                    </li>

                    <li>
                        <!-- Rótulo estilizado para o checkbox da opção 'Executável (Windows)' -->
                        <label class="cyberpunk-checkbox-label">

                            <!-- Checkbox para a opção 'Executável (Windows)' -->
                            <input type="checkbox" class="cyberpunk-checkbox" id="app_exe" name="app_exe">

                            <!-- Texto associado ao checkbox, indicando a opção 'Executável (Windows)' -->
                            <span><strong>Executável </strong>(Windows)</span>
                        </label>
                    </li>

                    <li>
                        <!-- Div com a classe 'form-group' para agrupar o campo de entrada de detalhes -->
                        <div class="form-group">
                            <!-- Campo de entrada de texto para adicionar observações/detalhes sobre a aplicação, com a classe 'form-style' para estilização. O campo é obrigatório -->
                            <input type="text" class="form-style" placeholder="Detalhes..." id="app_obs" name="app_obs" required>
                            
                            <!-- Ícone ao lado do campo de texto, estilizado com as classes 'input-icon' e 'uil uil-user' -->
                            <i class="input-icon uil uil-user"></i>                 
                        </div>
                    </li>
                    <li>
                        <!-- Rótulo estilizado indicando que a próxima seção se refere à complexidade da aplicação -->
                        <label class="cyberpunk-checkbox-label">
                            
                            <!-- Texto indicando a complexidade da aplicação -->
                            <span><strong>Complexidade</strong> da aplicação.</span>
                        </label>
                    </li>

                    <li>
                        <!-- Campo de entrada do tipo 'range' (slider) para selecionar a complexidade da aplicação. O valor padrão é 50, com um mínimo de 0 e um máximo de 100 -->
                        <input id="app_complex" name="app_complex" class="slider" value="50" max="100" min="0" type="range">    
                    </li>
                </ul>

                <!-- Botão de envio do formulário, estilizado com a classe 'button'. O texto do botão é 'Solicitar Aplicação' -->
                <button class="button" type="submit" href="">Solicitar Aplicação</button>
            </form>
        </div> <!-- Fecha a div 'inner' que contém o formulário e o texto informativo. -->
    </div> <!-- Fecha a div 'plan' que envolve a seção principal do formulário. -->
</div> <!-- Fecha a div 'master' que agrupa todo o conteúdo da página. -->
{% endblock %} <!-- Fecha o bloco 'content'. -->
```


```html
<!-- user.html -->
```

## app / controllers / default.py

```python
from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.tables import Cliente, Servico

# Cria um Blueprint para o módulo 'default'
default = Blueprint('default', __name__)

# Decorador que verifica se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Redireciona pra página inicial se o usuário não estiver logado
        if 'username' not in session:
            return redirect(url_for('default.index'))
        return f(*args, **kwargs)
    return decorated_function

# Rota para a página inicial
@default.route('/', methods=['GET', 'POST'])
def index():
    # Se o método da requisição for POST
    if request.method == 'POST': 
        print(request.form) # Imprime os dados do formulário no console

        # Verifica se o email foi enviado
        if 'email' in request.form: 
            fullname = request.form['fullname'] # Obtém o nome completo
            username = request.form['username'] # Obtém o nome de usuário
            email = request.form['email'] # Obtém o e-mail
            password = request.form['password'] # Obtém a senha
            
            # Verifica se o nome de usuário já existe no banco de dados
            user = Cliente.query.filter_by(username=username).first()
            if user:
                error = ['register', 'Esse nome de usuário já existe. Por favor, escolha outro.']
                return render_template('index.html', error=error)# Retorna erro na tela de registro
            else:
                # Verifica se o email já está em uso
                user = Cliente.query.filter_by(email=email).first()
                if user:
                    error = ['register', 'Esse E-mail já está sendo utilizado. Por favor, escolha outro.']
                    return render_template('index.html', error=error) # Retorna erro na tela de registro
                else:
                    # Cria um novo usuário se não houver conflitos
                    hashed_password = generate_password_hash(password) # Criptografa a senha
                    new_user = Cliente(fullname=fullname, username=username, email=email, senha=hashed_password)
                    session['user_id'] = new_user.id # Armazena o ID do usuário na sessão pra segurança
                    session['username'] = new_user.username # Armazena o nome de usuário na sessão pra conveniência
                    db.session.add(new_user)  # Adiciona o novo usuário à sessão do banco de dados
                    db.session.commit() # Salva as alterações no banco de dados
                    return redirect(url_for('default.user', username=username)) # Redireciona pra página do usuário
        else:
            # Processo de login
            username = request.form['username'] # Obtém o nome de usuário
            password = request.form['password'] # Obtém a senha
            user = Cliente.query.filter_by(username=username).first() # Busca o usuário pelo nome de usuário

            # Verifica se a senha está correta
            if user and check_password_hash(user.senha, password): 
                session['user_id'] = user.id # Armazena o ID do usuário na sessão
                session['username'] = user.username # Armazena o nome de usuário na sessão
                return redirect(url_for('default.user', username=username)) # Redireciona para a página do usuário
            else:
                error = ['login', 'Nome de usuário ou senha incorretos.'] # Mensagem de erro se login falhar
                return render_template('index.html', error=error) # Retorna erro na tela de login
    else:  # Se o método for GET
        if 'username' not in session:
            return render_template('index.html') # Exibe a página de login
        else:
            return redirect(url_for('default.user', username=session['username'])) # Redireciona pra página do usuário logado

# Rota para logout
@default.route('/logout')
def logout():
    session.clear() # Limpa a sessão do usuário
    return redirect(url_for('default.index')) # Redireciona pra página inicial

# Rota para a página do usuário
@default.route('/user/<username>', methods=['GET', 'POST'])
@login_required # Garante que o usuário esteja logado

def user(username):
    if request.method == 'POST': # Se o método da requisição for POST
        print(request.form) # Imprime os dados do formulário no console

        # Verifica se o nome do serviço foi enviado
        if 'service_name' in request.form: 
            service_name = request.form['service_name'] # Obtém o nome do serviço
            service = Servico.query.filter_by(name=service_name).first() 

            # Verifica se o serviço já existe
            if service:
                error = ['service_name', 'Você já possui um serviço com esse nome. Por favor, escolha outro.']
                return render_template('user.html', error=error) # Retorna erro se o serviço já existir
            else:
                client_id = session['user_id'] # Obtém o ID do cliente da sessão

                # Verifica quais opções foram selecionadas no formulário
                app_web = request.form['app_web']  
                app_android = request.form['app_android']  
                app_IOS = request.form['app_IOS']  
                app_exe = request.form['app_exe']  
                app_complex = request.form['app_complex'] # Obtém a complexidade da aplicação

                # Cria um novo serviço
                new_service = Servico(name=service_name, cliente_id=client_id, app_web=app_web, app_android=app_android, app_IOS=app_IOS, app_exe=app_exe, app_complex=app_complex)
                db.session.add(new_service) # Adiciona o novo serviço à sessão do banco de dados
                db.session.commit() # Salva as alterações no banco de dados
                services = Servico.query.filter_by(cliente_id=user.id).all() # Busca todos os serviços do cliente
                return render_template('user.html', services=services) # Exibe a página do usuário com os serviços

        elif 'service_edit' in request.form:  # Se o formulário de edição de serviço foi enviado
            user = Cliente.query.filter_by(username=username).first_or_404()  # Busca o usuário pelo nome
            services = Servico.query.filter_by(cliente_id=user.id).all()  # Busca todos os serviços do cliente
            print(user)

            # Exibe a página do usuário para edição
            return render_template('user.html', user=user, services=services, service_id=request.form['service_edit'])  

    else:  # Se o método for GET
        user = Cliente.query.filter_by(username=username).first_or_404() # Busca o usuário pelo nome
        services = Servico.query.filter_by(cliente_id=user.id).all() # Busca todos os serviços do cliente
        print(user)

        # Exibe a página do usuário com os serviços
        return render_template('user.html', user=user, services=services, service_id=None)  

# Rota para adicionar um novo serviço
@default.route('/user/add_service', methods=['GET', 'POST'])
@login_required # Garante que o usuário esteja logado

def add_service():
    if request.method == 'POST': # Se o método da requisição for POST
        print(request.form) # Imprime os dados do formulário no console

        # Verifica se o nome do serviço foi enviado
        if 'service_name' in request.form: 
            service_name = request.form['service_name'] # Obtém o nome do serviço
            service = Servico.query.filter_by(name=service_name).first() 

            # Verifica se o serviço já existe
            if service:
                error = ['service_name', 'Você já possui um serviço com esse nome. Por favor, escolha outro.']
                return render_template('user.html', error=error) # Retorna erro se o serviço já existir
            else:
                client_id = session['user_id'] # Obtém o ID do cliente da sessão

                # Verifica quais opções foram selecionadas no formulário
                if 'app_web' in request.form:
                    app_web = True
                else:
                    app_web = False
                if 'app_android' in request.form:
                    app_android = True
                else:
                    app_android = False
                if 'app_IOS' in request.form:
                    app_IOS = True
                else:
                    app_IOS = False
                if 'app_exe' in request.form:
                    app_exe = True
                else:
                    app_exe = False

                app_complex = request.form['app_complex'] # Obtém a complexidade da aplicação
                app_obs = request.form['app_obs'] # Obtém observações sobre a aplicação

                # Cria um novo serviço
                new_service = Servico(name=service_name, status='Pendente', cliente_id=client_id, app_web=app_web, app_android=app_android, app_IOS=app_IOS, app_exe=app_exe, app_complex=app_complex
```


## app / models / tables.py

```python
from app import db

# Classe representando o modelo Cliente na base de dados
class Cliente(db.Model):

    # Definição das colunas da tabela 'Cliente'
    id = db.Column(db.Integer, primary_key=True) # Coluna 'id' como chave primária, do tipo inteiro
    username = db.Column(db.String(80), nullable=False) # Coluna 'username' do tipo string, não pode ser nula
    fullname = db.Column(db.String(80), nullable=False) # Coluna 'fullname' do tipo string, não pode ser nula
    email = db.Column(db.String(120), unique=True, nullable=False) # Coluna 'email' do tipo string, deve ser única e não pode ser nula
    senha = db.Column(db.String(120), nullable=False) # Coluna 'senha' do tipo string, não pode ser nula

    # Definição do relacionamento entre 'Cliente' e 'Servico', onde um cliente pode ter vários serviços
    services = db.relationship('Servico', backref='cliente', lazy=True)

    # Método especial para representar a instância de 'Cliente' como uma string
    def __repr__(self):
        return f'<Cliente {self.username}>'

    # Método para converter a instância de 'Cliente' em um dicionário (útil para serialização)
    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "username": self.username,
            "email": self.email,
            "senha": self.senha
        }

# Classe representando o modelo Servico na base de dados
class Servico(db.Model):

    # Definição das colunas da tabela 'Servico'
    id = db.Column(db.Integer, primary_key=True) # Coluna 'id' como chave primária, do tipo inteiro
    name = db.Column(db.String(80), nullable=False) # Coluna 'name' do tipo string, não pode ser nula
    status = db.Column(db.String(20), nullable=False) # Coluna 'status' do tipo string, não pode ser nula

    # Chave estrangeira referenciando a tabela 'Cliente', indicando qual cliente possui o serviço
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    # Colunas booleanas indicando as plataformas nas quais o serviço vai ser disponibilizado
    app_web = db.Column(db.Boolean, default=False)
    app_android = db.Column(db.Boolean, default=False)
    app_IOS = db.Column(db.Boolean, default=False)
    app_exe = db.Column(db.Boolean, default=False)

    # Coluna que armazena a complexidade do aplicativo, representada por um valor inteiro
    app_complex = db.Column(db.Integer, nullable=True)

    # Coluna para armazenar observações adicionais sobre o serviço
    obs = db.Column(db.String(200), nullable=False)
    
    # Método especial para representar a instância de 'Servico' como uma string
    def __repr__(self):
        return f'<Servico {self.name}>'

    # Método para converter a instância de 'Servico' em um dicionário (útil para serialização)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cliente_id": self.cliente_id,
            "app_web": self.app_web,
            "app_android": self.app_android,
            "app_IOS": self.app_IOS,
            "app_exe": self.app_exe,
            "app_complex": self.app_complex
        }
```


## app / __init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criação da aplicação Flask
app = Flask(__name__)

# Definição de uma chave secreta para a aplicação (usada para sessões, cookies, etc.)
app.secret_key = '9nu%-QtE#15p$C9_w;!?U2I4ArtH7<(1*p8A[!#3#%wP+'

# Configuração do URI do banco de dados. O banco de dados é SQLite e será armazenado no arquivo 'data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Desativação da sinalização de modificações no SQLAlchemy para evitar overhead desnecessário 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instanciação do objeto SQLAlchemy, que gerencia a comunicação com o banco de dados
db = SQLAlchemy(app)

# Importa e registra o blueprint 'default' da aplicação, que contém rotas específicas definidas no módulo `default`
from app.controllers.default import default
app.register_blueprint(default)

# Importa a classe 'Cliente' do módulo 'tables' dentro do pacote 'models'. Este é o modelo do banco de dados que foi definido anteriormente
from app.models.tables import Cliente  # Import your model

# Cria o contexto da aplicação para operações que dependem da aplicação estar rodando, como a criação do banco de dados
with app.app_context():
    # Cria todas as tabelas definidas nos modelos do SQLAlchemy, se elas ainda não existirem
    db.create_all()
```

## app / static / css / style.css

```css

```