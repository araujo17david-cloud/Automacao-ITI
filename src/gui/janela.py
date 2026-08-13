import customtkinter as ctk

from src.components.menu import criar_menu
from src.components.splash import SplashScreen
from src.components.statusbar import StatusBar
from src.pages.configuracoes import (
    criar_pagina_configuracoes
)
from src.pages.relatorios import (
    criar_pagina_relatorios
)
from src.pages.sobre import (
    criar_pagina_sobre
)
from src.services.config_service import (
    carregar_config
)
from src.services.logger_service import logger
from src.utils.caminhos import (
    CAMINHO_ICONE,
    CAMINHO_LOGO
)
from src.version import (
    APP_NAME,
    VERSION
)


def iniciar():
    logger.info(
        "=" * 60
    )

    logger.info(
        f"Iniciando {APP_NAME} v{VERSION}"
    )

    config = carregar_config()

    ctk.set_appearance_mode(
        config.get(
            "tema",
            "Light"
        )
    )

    ctk.set_default_color_theme(
        "blue"
    )

    janela = ctk.CTk()

    janela.title(
        f"{APP_NAME} v{VERSION}"
    )

    janela.geometry(
        "1280x760"
    )

    janela.minsize(
        1100,
        700
    )

    # ==================================
    # SPLASH SCREEN
    # ==================================

    splash = SplashScreen(
        janela,
        CAMINHO_LOGO
    )

    try:
        splash.atualizar(
            "Carregando interface...",
            0.25
        )

        # ==================================
        # ÍCONE DA JANELA
        # ==================================

        if CAMINHO_ICONE.exists():
            try:
                janela.iconbitmap(
                    str(CAMINHO_ICONE)
                )

            except Exception as erro_icone:
                logger.warning(
                    "Não foi possível carregar "
                    f"o ícone: {erro_icone}"
                )

        # ==================================
        # CONFIGURAÇÃO DA JANELA
        # ==================================

        janela.grid_columnconfigure(
            1,
            weight=1
        )

        janela.grid_rowconfigure(
            0,
            weight=1
        )

        janela.grid_rowconfigure(
            1,
            weight=0
        )

        # ==================================
        # MENU LATERAL
        # ==================================

        menu = criar_menu(
            janela,
            CAMINHO_LOGO
        )

        splash.atualizar(
            "Carregando menu...",
            0.45
        )

        botao_relatorios = menu[
            "relatorios"
        ]

        botao_configuracoes = menu[
            "configuracoes"
        ]

        botao_sobre = menu[
            "sobre"
        ]

        # ==================================
        # ÁREA PRINCIPAL
        # ==================================

        area_principal = ctk.CTkFrame(
            janela,
            corner_radius=0,
            fg_color="#F4F6F8"
        )

        area_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        area_principal.grid_columnconfigure(
            0,
            weight=1
        )

        area_principal.grid_rowconfigure(
            0,
            weight=1
        )

        # ==================================
        # BARRA DE STATUS
        # ==================================

        statusbar = StatusBar(
            janela
        )

        statusbar.frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        splash.atualizar(
            "Carregando componentes...",
            0.60
        )

        # ==================================
        # PÁGINAS
        # ==================================

        pagina_relatorios = (
            criar_pagina_relatorios(
                area_principal,
                statusbar
            )
        )

        pagina_configuracoes = (
            criar_pagina_configuracoes(
                area_principal
            )
        )

        pagina_sobre = (
            criar_pagina_sobre(
                area_principal,
                CAMINHO_LOGO
            )
        )

        splash.atualizar(
            "Finalizando...",
            0.90
        )

        # ==================================
        # NAVEGAÇÃO
        # ==================================

        def mostrar_relatorios():
            pagina_relatorios.tkraise()

            botao_relatorios.configure(
                fg_color="#1D6B47"
            )

            botao_configuracoes.configure(
                fg_color="transparent"
            )

            botao_sobre.configure(
                fg_color="transparent"
            )

        def mostrar_configuracoes():
            pagina_configuracoes.tkraise()

            botao_relatorios.configure(
                fg_color="transparent"
            )

            botao_configuracoes.configure(
                fg_color="#1D6B47"
            )

            botao_sobre.configure(
                fg_color="transparent"
            )

        def mostrar_sobre():
            pagina_sobre.tkraise()

            botao_relatorios.configure(
                fg_color="transparent"
            )

            botao_configuracoes.configure(
                fg_color="transparent"
            )

            botao_sobre.configure(
                fg_color="#1D6B47"
            )

        # ==================================
        # CONECTAR BOTÕES
        # ==================================

        botao_relatorios.configure(
            command=mostrar_relatorios
        )

        botao_configuracoes.configure(
            command=mostrar_configuracoes
        )

        botao_sobre.configure(
            command=mostrar_sobre
        )

        # ==================================
        # PÁGINA INICIAL
        # ==================================

        mostrar_relatorios()

        splash.atualizar(
            "Pronto!",
            1
        )

        janela.update_idletasks()

    except Exception:
        logger.exception(
            "Erro durante a inicialização "
            "da aplicação."
        )

        raise

    finally:
        try:
            splash.fechar()
        except Exception:
            pass

    # ==================================
    # COLOCAR JANELA EM PRIMEIRO PLANO
    # ==================================

    janela.lift()
    janela.focus_force()

    # ==================================
    # ENCERRAMENTO
    # ==================================

    def fechar_aplicacao():
        logger.info(
            f"Encerrando {APP_NAME} v{VERSION}"
        )

        janela.destroy()

    janela.protocol(
        "WM_DELETE_WINDOW",
        fechar_aplicacao
    )

    # ==================================
    # INICIAR APLICAÇÃO
    # ==================================

    janela.mainloop()