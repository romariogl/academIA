import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "./App.css";

function AcademIA() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isChatOpen, setIsChatOpen] = useState(false);

  const BACKEND_URL = "http://127.0.0.1:5000";
  const chatEndRef = useRef(null);

  useEffect(() => {
    const initialMessage = {
      sender: "bot",
      text: `
      <p><strong>Bem-vindo ao Portal de Periódicos da CAPES com IA!</strong></p>
      <p>Eu sou a <strong>Academ.ia</strong>, sua assistente virtual para pesquisa acadêmica.</p>
      <p>Posso te ajudar com:</p>
      <ul>
        <li>Buscar artigos sobre inteligência artificial</li>
        <li>Responder perguntas sobre conteúdo específico</li>
        <li>Fornecer informações sobre pesquisas acadêmicas</li>
      </ul>
      <p>Como posso te ajudar hoje?</p>
      `,
    };
    setMessages([initialMessage]);
  }, []);

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "user", text: input }]);
      const userInput = input;
      setInput("");

      try {
        const response = await axios.post(`${BACKEND_URL}/rag`, { query: userInput });
        const botResponse = response.data.answer || "Erro ao gerar resposta";
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: botResponse },
        ]);
      } catch (error) {
        console.error("Erro ao se conectar com o backend:", error);
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "Erro ao obter a resposta. Tente novamente." },
        ]);
      }
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="academia-app">
      {/* Header do Governo */}
      <div className="container-fluid bg-white">
        <div className="container">
          <div className="row align-items-center barra-gov-br">
            <div className="col-4">
              <div className="row align-items-center">
                <div className="col">
                  <a href="https://www.gov.br/" target="_blank" className="logo-barra-gov-br">
                    <i className="fas fa-university" style={{fontSize: '24px', color: '#1c1c5c', marginRight: '10px'}}></i>
                    <span style={{fontSize: '14px', fontWeight: 'bold', color: '#1c1c5c'}}>Governo Federal</span>
                  </a>
                </div>
                <div className="col-8 d-none d-md-none d-lg-block">
                  <a href="https://www.gov.br/capes" target="_blank" className="barra-gov-br-nome-orgao">
                    Ministério da Educação/CAPES
                  </a>
                </div>
              </div>
            </div>
            <div className="col">
              <nav className="bg-white">
                <ul className="nav justify-content-end align-items-center">
                  <li className="barra-gov-br-nav-item d-none d-md-none d-lg-block">
                    <a className="barra-gov-br-nav-link" href="https://www.gov.br/pt-br/orgaos-do-governo" target="_blank">Órgãos do Governo</a>
                  </li>
                  <li className="barra-gov-br-nav-item d-none d-md-none d-lg-block">
                    <a className="barra-gov-br-nav-link" href="https://www.gov.br/acessoainformacao/pt-br" target="_blank">Acesso à Informação</a>
                  </li>
                  <li className="barra-gov-br-nav-item d-none d-md-none d-lg-block">
                    <a className="barra-gov-br-nav-link" href="http://www4.planalto.gov.br/legislacao" target="_blank">Legislação</a>
                  </li>
                  <li className="barra-gov-br-nav-item d-none d-md-none d-lg-block">
                    <a className="barra-gov-br-nav-link" href="https://www.gov.br/governodigital/pt-br/acessibilidade-digital" target="_blank">Acessibilidade</a>
                  </li>
                  <li className="barra-gov-br-nav-item">
                    <a className="barra-gov-br-nav-link contraste" href="#"><i className="fas fa-adjust"></i></a>
                  </li>
                  <li className="barra-gov-br-nav-item">
                    <a className="btn barra-gov-br-btn-entrar btn-sm w-100" href="https://acesso.gov.br/" role="button" target="_blank">
                      <i className="fas fa-user"></i> Entrar
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>

      {/* Header Principal */}
      <div className="container-fluid">
        <header className="row shadow-sm">
          <div className="container mx-top-header">
            <div className="row align-items-center">
              <div className="col-2 col-sm-1 d-block d-lg-none">
                <a className="navbar-toggler" href="#drawerMenu" data-toggle="drawer" data-target="#drawerMenu" aria-controls="drawerMenu" aria-label="Toggle navigation">
                  <span className="fas fa-align-justify"></span>
                </a>
              </div>
              <div className="logos-principais col-10 col-sm-9 col-lg-4">
                <div className="row align-items-center">
                  <div className="col-5">
                    <a target="_blank" href="https://www.gov.br/capes/pt-br" title="Coordenação de Aperfeiçoamento de Pessoal de Nível Superior" style={{textDecoration: 'none'}}>
                      <i className="fas fa-graduation-cap" style={{fontSize: '32px', color: '#1c1c5c'}}></i>
                      <span style={{fontSize: '16px', fontWeight: 'bold', color: '#1c1c5c', marginLeft: '5px'}}>CAPES</span>
                    </a>
                  </div>
                  <div className="col">
                                      <a target="_self" href="/" title="Voltar para a página inicial" style={{textDecoration: 'none'}}>
                    <i className="fas fa-book-open" style={{fontSize: '36px', color: '#1c1c5c'}}></i>
                    <span style={{fontSize: '18px', fontWeight: 'bold', color: '#1c1c5c', marginLeft: '5px'}}>Portal de Periódicos</span>
                  </a>
                  </div>
                </div>
              </div>
              <div className="col-12 col-sm-6 col-md-7 col-lg-6 d-none d-md-none d-lg-block">
                <nav className="navbar navbar-expand-lg">
                  <div className="collapse navbar-collapse justify-content-end menu-horizontal" id="navbarNav">
                    <ul className="nav menu mod-list">
                      <li className="item-646 deeper parent">
                        <a href="#">Sobre</a>
                        <ul className="nav-child unstyled small">
                          <li className="item-722"><a href="#">Acesso Aberto</a></li>
                          <li className="item-647"><a href="#">Quem somos</a></li>
                          <li className="item-652"><a href="#">Missão e objetivos</a></li>
                        </ul>
                      </li>
                      <li className="item-648 deeper parent">
                        <a href="#">Acervo</a>
                        <ul className="nav-child unstyled small">
                          <li className="item-699"><a href="#">Buscar assunto</a></li>
                          <li className="item-700"><a href="#">Lista de bases e coleções</a></li>
                        </ul>
                      </li>
                      <li className="item-649 deeper parent">
                        <a href="#">Treinamentos</a>
                        <ul className="nav-child unstyled small">
                          <li className="item-658"><a href="#">Calendário</a></li>
                          <li className="item-659"><a href="#">Materiais de apoio</a></li>
                        </ul>
                      </li>
                      <li className="item-650"><a href="#">Informativos</a></li>
                      <li className="item-651 deeper parent">
                        <a href="#">Ajuda</a>
                        <ul className="nav-child unstyled small">
                          <li className="item-660"><a href="#">Perguntas frequentes</a></li>
                          <li className="item-661"><a href="#">Suporte regional</a></li>
                          <li className="item-662"><a href="#">Fale conosco</a></li>
                        </ul>
                      </li>
                    </ul>
                  </div>
                </nav>
              </div>
              <div className="col">
                <div className="dropdown">
                  <a
                    role="button"
                    data-message="Botão para realizar o login no meu espaço"
                    id="bt-meu-espaco-login"
                    className="btn btn-outline-padrao py-2 float-right"
                    data-toggle="dropdown"
                    href="#"
                    aria-haspopup="true" 
                    aria-expanded="false">Meu espaço
                  </a>
                  <div className="border-0 shadow-sm dropdown-menu-right dropdown-menu dropdown-menu-lg-left" aria-labelledby="bt-meu-espaco-login" role="alert" aria-live="assertive" aria-atomic="true" id="card-login">
                    <div className="card-body" id="body-login">
                      <h5 className="card-title mb-4 mt-4">Entrar</h5>
                      <form id="form-login" name="frmLogin" action="#" method="post">
                        <div className="form-row">
                          <div className="col-md-12">
                            <label className="sr-only" htmlFor="usuario">Nome do usuário</label>
                            <div className="inner-addon left-addon">
                              <i className="fas fa-user"></i>
                              <input type="text" name="username" className="form-control mb-3 border-0 bg-input-login" id="usuario" placeholder="Nome do usuário" required />
                            </div>
                          </div>
                          <div className="col-md-12">
                            <label className="sr-only" htmlFor="senha">Senha</label>
                            <div className="inner-addon left-addon">
                              <i className="fas fa-lock"></i>
                              <input type="password" name="password" className="form-control mb-3 border-0 bg-input-login" id="senha" placeholder="Senha" required />
                            </div>
                          </div>
                          <div className="col-md-12 mb-3">
                            <small><a href="#" title="Esqueci minha senha">Esqueci minha senha</a></small>
                          </div>
                          <div className="col-md-12">
                            <button type="submit" className="btn btn-primary mb-2 w-100" data-message="Botão para Entrar">Entrar</button>
                            <small>Não possui acesso? <a href="#" target="_self">Registre-se</a></small>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>
      </div>

      {/* Área de Busca e IA */}
      <div className="row bg-busca-img p-3">
        <div className="container mp">
          <div className="row justify-content-center">
            <div className="col-lg-7 col-12 col-sm-12">
              <div className="area-busca mb-5">
                <div className="position-relative">
                  <form action="" method="GET" id="busca" className="busca" data-gtm-form-interact-id="0">
                    <div className="search-default">
                      <button type="submit" className="btn" id="btn-busca-primo" value="Submit">
                        <i className="fas fa-search"></i>
                      </button>
                      <input name="q" type="search" id="input-busca-primo" className="form-control" placeholder="O que você está procurando?" minLength="4" required data-gtm-form-interact-field-id="0" />
                    </div>
                  </form>
                  
                  <div className="ia-section mt-4">
                    <div className="text-center">
                      <div className="ia-info mb-3">
                        <h4 className="text-white mb-2">🤖 Academ.ia</h4>
                        <p className="text-white-50 mb-3">Sua assistente virtual para pesquisa acadêmica</p>
                      </div>
                      
                      <button 
                        className="btn btn-outline-padrao mb-3 mx-auto"
                        onClick={() => setIsChatOpen(!isChatOpen)}
                      >
                        <i className="fas fa-robot"></i>
                        Para uma melhor experiência de busca, utilize a nossa <strong>IA</strong>!
                      </button>
                      
                      <div className="ia-features">
                        <div className="row">
                          <div className="col-md-4">
                            <i className="fas fa-search text-white-50"></i>
                            <p className="text-white-50">Busca Inteligente</p>
                          </div>
                          <div className="col-md-4">
                            <i className="fas fa-brain text-white-50"></i>
                            <p className="text-white-50">IA Generativa</p>
                          </div>
                          <div className="col-md-4">
                            <i className="fas fa-graduation-cap text-white-50"></i>
                            <p className="text-white-50">Conteúdo Acadêmico</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Chat da IA */}
      {isChatOpen && (
        <div className="chat-overlay">
          <div className="chat-container">
            <div className="chat-header">
              <h5>Academ.ia - Assistente Virtual</h5>
              <button 
                className="btn-close"
                onClick={() => setIsChatOpen(false)}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="chat-body">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`message ${msg.sender === "user" ? "user-message" : "bot-message"}`}
                >
                  <div className="message-content">
                    {msg.sender === "user" ? (
                      msg.text
                    ) : (
                      <div dangerouslySetInnerHTML={{ __html: msg.text }} />
                    )}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef}></div>
            </div>
            <div className="chat-footer">
              <div className="input-group">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Digite sua pergunta..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSend()}
                />
                <button
                  className="btn btn-primary"
                  type="button"
                  onClick={handleSend}
                >
                  <i className="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Seção de Treinamentos */}
      <div className="row bg-padrao p-3">
        <div className="container mp">
          <div className="row">
            <div className="col-md-6">
              <h3 className="text-light">Treinamentos</h3>
              <hr />
            </div>
          </div>
          <div className="row justify-content-center">
            <div className="col-10">
              <div className="row">
                <div className="col-md-6">
                  <p className="h4 text-light">Quer aprender a pesquisar no Portal de Periódicos da CAPES?</p>
                  <p className="text-light">Participe dos treinamentos e otimize sua busca. As inscrições são gratuitas e as turmas oferecidas por área do conhecimento, para um melhor aproveitamento dos conteúdos.</p>
                  <p><span style={{color: '#ffffff'}}><a className="p-2 btn btn-link-fundo-padrao" href="#">Acesse o calendário</a></span></p>
                </div>
                <div className="col-lg-6 d-none d-md-none d-lg-block">
                  <div style={{textAlign: 'center', padding: '20px'}}>
                    <i className="fas fa-graduation-cap" style={{fontSize: '48px', color: 'white'}}></i>
                    <p style={{color: 'white', marginTop: '10px', fontSize: '18px'}}>Treinamentos</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="row bg-white menu-footer py-5">
        <div className="container">
          <div className="row">
            <div className="col-md-3 col-12 d-sm-none d-md-block navegue-menu mb-4">
              <p className="h4 text-dark"><i className="fas fa-location-arrow"></i> Navegue </p>
              <ul className="nav menu mod-list">
                <li><a href="#">Sobre</a></li>
                <li><a href="#">Acervo</a></li>
                <li><a href="#">Treinamentos</a></li>
                <li><a href="#">Informativos</a></li>
              </ul>
            </div>
            <div className="col-md-3 col-12 d-sm-none d-md-block navegue-menu mb-4">
              <p className="h4 text-dark"><i className="fas fa-comment fa-flip-horizontal"></i> Ajuda </p>
              <ul className="nav menu mod-list">
                <li><a href="#">Perguntas frequentes</a></li>
                <li><a href="#">Suporte regional</a></li>
                <li><a href="#">Fale conosco</a></li>
              </ul>
            </div>
            <div className="col-md-6">
              <p className="h4 text-dark mb-3"><i className="fas fa-map-marker-alt"></i> Endereço </p>
              <p className="lead ml-4 endereco">
                Setor Bancário Norte (SBN), Quadra 2, Bloco L, Lote 06, Edifício CAPES.<br />
                Brasília, DF<br />
                CEP: 70.040-031
              </p>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <div className="float-right">
                <small className="text-muted">© 2024. Todos os direitos reservados.</small>
                <a href="#" className="ml-3 termo-uso">Termos de Uso</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Final */}
      <footer className="row bg-padrao footer d-flex">
        <div className="container">
          <div className="row">
            <div className="col-12 co-sm-6 col-md-6 col-lg-8">
              <a target="_blank" href="https://www.gov.br/acessoainformacao/pt-br" style={{marginRight: '20px'}}>
                <i className="fas fa-info-circle" style={{fontSize: '24px', color: 'white', marginRight: '5px'}}></i>
                <span style={{fontSize: '12px', color: 'white'}}>Acesso à Informação</span>
              </a>
              <a target="_blank" href="https://www.gov.br/capes/pt-br/acesso-a-informacao/sei" style={{marginRight: '20px'}}>
                <i className="fas fa-search" style={{fontSize: '24px', color: 'white', marginRight: '5px'}}></i>
                <span style={{fontSize: '12px', color: 'white'}}>SEI</span>
              </a>
              <a target="_blank" href="https://falabr.cgu.gov.br/publico/Manifestacao/SelecionarTipoManifestacao.aspx?ReturnUrl=%2f" style={{marginRight: '20px'}}>
                <i className="fas fa-comments" style={{fontSize: '24px', color: 'white', marginRight: '5px'}}></i>
                <span style={{fontSize: '12px', color: 'white'}}>Fala.BR</span>
              </a>
            </div>
            <div className="col-sm-6 col-md-6 col-lg-4">
              <div className="row">
                <div className="col-12 col-sm-4">
                  <a target="_blank" href="https://www.gov.br/capes/pt-br">
                    <i className="fas fa-graduation-cap" style={{fontSize: '32px', color: 'white'}}></i>
                    <span style={{fontSize: '14px', fontWeight: 'bold', color: 'white', marginLeft: '5px'}}>CAPES</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default AcademIA;