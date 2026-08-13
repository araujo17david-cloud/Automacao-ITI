import shutil
import subprocess
import sys

from pathlib import Path

from src.version import (
    APP_NAME,
    COMPANY,
    COPYRIGHT,
    DESCRIPTION,
    EXECUTABLE_NAME,
    VERSION
)


# ==================================
# CAMINHOS PRINCIPAIS
# ==================================

PASTA_PROJETO = Path(__file__).resolve().parent

PASTA_BUILD = (
    PASTA_PROJETO
    / "build"
)

PASTA_DIST = (
    PASTA_PROJETO
    / "dist"
)

PASTA_RELEASE = (
    PASTA_PROJETO
    / "release"
)

PASTA_BUILD_CONFIG = (
    PASTA_PROJETO
    / "build_config"
)

PASTA_ASSETS = (
    PASTA_PROJETO
    / "assets"
)

PASTA_INSTALLER = (
    PASTA_PROJETO
    / "installer"
)

PASTA_INSTALLER_OUTPUT = (
    PASTA_PROJETO
    / "installer_output"
)


# ==================================
# ARQUIVOS
# ==================================

ARQUIVO_SPEC = (
    PASTA_PROJETO
    / f"{EXECUTABLE_NAME}.spec"
)

ARQUIVO_VERSION_INFO = (
    PASTA_BUILD_CONFIG
    / "version_info.txt"
)

ARQUIVO_ISS = (
    PASTA_INSTALLER
    / "Automacao_ITI.iss"
)

CAMINHO_ICONE = (
    PASTA_ASSETS
    / "logo.ico"
)

CAMINHO_LOGO = (
    PASTA_ASSETS
    / "logo.png"
)


# ==================================
# LOCALIZAR INNO SETUP
# ==================================

def localizar_inno_setup():
    caminhos_possiveis = [
        Path(
            r"C:\Program Files\Inno Setup 6\ISCC.exe"
        ),
        Path(
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        ),
        (
            Path.home()
            / "AppData"
            / "Local"
            / "Programs"
            / "Inno Setup 6"
            / "ISCC.exe"
        )
    ]

    for caminho in caminhos_possiveis:
        if caminho.exists():
            return caminho

    raise FileNotFoundError(
        "O compilador do Inno Setup não foi encontrado.\n"
        "Verifique se o Inno Setup 6 está instalado."
    )


# ==================================
# VERSÃO WINDOWS
# ==================================

def obter_versao_windows():
    partes = VERSION.split(".")

    numeros = []

    for parte in partes:
        try:
            numeros.append(
                int(parte)
            )

        except ValueError:
            numeros.append(0)

    while len(numeros) < 4:
        numeros.append(0)

    return tuple(
        numeros[:4]
    )


# ==================================
# GERAR VERSION_INFO
# ==================================

def gerar_version_info():
    PASTA_BUILD_CONFIG.mkdir(
        parents=True,
        exist_ok=True
    )

    versao_windows = obter_versao_windows()

    versao_tupla = (
        f"({versao_windows[0]}, "
        f"{versao_windows[1]}, "
        f"{versao_windows[2]}, "
        f"{versao_windows[3]})"
    )

    conteudo = f"""VSVersionInfo(
    ffi=FixedFileInfo(
        filevers={versao_tupla},
        prodvers={versao_tupla},
        mask=0x3F,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct(
                            'CompanyName',
                            '{COMPANY}'
                        ),
                        StringStruct(
                            'FileDescription',
                            '{DESCRIPTION}'
                        ),
                        StringStruct(
                            'FileVersion',
                            '{VERSION}'
                        ),
                        StringStruct(
                            'InternalName',
                            '{EXECUTABLE_NAME}'
                        ),
                        StringStruct(
                            'LegalCopyright',
                            '{COPYRIGHT}'
                        ),
                        StringStruct(
                            'OriginalFilename',
                            '{EXECUTABLE_NAME}.exe'
                        ),
                        StringStruct(
                            'ProductName',
                            '{APP_NAME}'
                        ),
                        StringStruct(
                            'ProductVersion',
                            '{VERSION}'
                        )
                    ]
                )
            ]
        ),
        VarFileInfo(
            [
                VarStruct(
                    'Translation',
                    [1033, 1200]
                )
            ]
        )
    ]
)
"""

    ARQUIVO_VERSION_INFO.write_text(
        conteudo,
        encoding="utf-8"
    )

    print(
        "[OK] Metadados do Windows gerados."
    )


# ==================================
# LIMPAR BUILD ANTERIOR
# ==================================

def limpar_build_anterior():
    print(
        "[INFO] Limpando compilação anterior..."
    )

    if PASTA_BUILD.exists():
        shutil.rmtree(
            PASTA_BUILD
        )

    if PASTA_DIST.exists():
        shutil.rmtree(
            PASTA_DIST
        )

    if PASTA_INSTALLER_OUTPUT.exists():
        shutil.rmtree(
            PASTA_INSTALLER_OUTPUT
        )

    if ARQUIVO_SPEC.exists():
        ARQUIVO_SPEC.unlink()

    print(
        "[OK] Limpeza concluída."
    )


# ==================================
# VERIFICAR ARQUIVOS
# ==================================

def verificar_arquivos():
    arquivos_obrigatorios = [
        PASTA_PROJETO / "main.py",
        CAMINHO_LOGO,
        CAMINHO_ICONE
    ]

    for arquivo in arquivos_obrigatorios:
        if not arquivo.exists():
            raise FileNotFoundError(
                "Arquivo obrigatório não encontrado: "
                f"{arquivo}"
            )

    print(
        "[OK] Arquivos necessários encontrados."
    )


# ==================================
# EXECUTAR PYINSTALLER
# ==================================

def executar_pyinstaller():
    print(
        "[INFO] Gerando executável..."
    )

    comando = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",

        "--name",
        EXECUTABLE_NAME,

        "--icon",
        str(CAMINHO_ICONE),

        "--version-file",
        str(ARQUIVO_VERSION_INFO),

        "--add-data",
        f"{PASTA_ASSETS};assets",

        str(
            PASTA_PROJETO
            / "main.py"
        )
    ]

    subprocess.run(
        comando,
        cwd=PASTA_PROJETO,
        check=True
    )

    executavel = (
        PASTA_DIST
        / f"{EXECUTABLE_NAME}.exe"
    )

    if not executavel.exists():
        raise FileNotFoundError(
            "O PyInstaller terminou, mas "
            "o executável não foi encontrado."
        )

    print(
        f"[OK] Executável criado: {executavel}"
    )

    return executavel


# ==================================
# CRIAR RELEASE
# ==================================

def criar_release(
    executavel
):
    pasta_release = (
        PASTA_RELEASE
        / f"{EXECUTABLE_NAME}_{VERSION}"
    )

    if pasta_release.exists():
        shutil.rmtree(
            pasta_release
        )

    pasta_release.mkdir(
        parents=True,
        exist_ok=True
    )

    destino_exe = (
        pasta_release
        / f"{EXECUTABLE_NAME}.exe"
    )

    shutil.copy2(
        executavel,
        destino_exe
    )

    # ==================================
    # VERSAO.TXT
    # ==================================

    arquivo_versao = (
        pasta_release
        / "VERSAO.txt"
    )

    arquivo_versao.write_text(
        (
            f"{APP_NAME}\n"
            f"Versão: {VERSION}\n"
            f"Empresa: {COMPANY}\n"
        ),
        encoding="utf-8"
    )

    # ==================================
    # LEIA-ME
    # ==================================

    arquivo_leia_me = (
        pasta_release
        / "LEIA-ME.txt"
    )

    conteudo_leia_me = (
        f"{APP_NAME}\n"
        f"{'=' * len(APP_NAME)}\n\n"

        f"Versão: {VERSION}\n"
        f"Empresa: {COMPANY}\n\n"

        f"{DESCRIPTION}\n\n"

        "EXECUÇÃO\n"
        "--------\n"
        f"Execute {EXECUTABLE_NAME}.exe "
        "para iniciar a aplicação.\n\n"

        "RELATÓRIOS\n"
        "----------\n"
        "A pasta padrão dos relatórios pode "
        "ser definida na tela Configurações.\n\n"

        "GERAÇÃO AUTOMÁTICA\n"
        "------------------\n"
        "A aplicação permite configurar uma "
        "geração automática mensal utilizando "
        "o Agendador de Tarefas do Windows.\n\n"

        "SUPORTE\n"
        "-------\n"
        "Em caso de erro, consulte os arquivos "
        "de log gerados pela aplicação.\n"
    )

    arquivo_leia_me.write_text(
        conteudo_leia_me,
        encoding="utf-8"
    )

    print(
        f"[OK] Release criada: {pasta_release}"
    )

    return pasta_release


# ==================================
# GERAR SCRIPT INNO SETUP
# ==================================

def gerar_script_instalador():
    PASTA_INSTALLER.mkdir(
        parents=True,
        exist_ok=True
    )

    conteudo = f"""
#define MyAppName "{APP_NAME}"
#define MyAppVersion "{VERSION}"
#define MyAppPublisher "{COMPANY}"
#define MyAppExeName "{EXECUTABLE_NAME}.exe"

[Setup]
AppId={{{{7D24F361-7FA9-4A32-A364-20260813A001}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}

DefaultDirName={{autopf}}\\Automacao ITI
DefaultGroupName={{#MyAppName}}

OutputDir=..\\installer_output
OutputBaseFilename=Automacao_ITI_Setup_{{#MyAppVersion}}

SetupIconFile=..\\assets\\logo.ico

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=admin

UninstallDisplayIcon={{app}}\\{{#MyAppExeName}}

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"

[Files]
Source: "..\\release\\{EXECUTABLE_NAME}_{VERSION}\\{EXECUTABLE_NAME}.exe"; DestDir: "{{app}}"; Flags: ignoreversion

Source: "..\\release\\{EXECUTABLE_NAME}_{VERSION}\\LEIA-ME.txt"; DestDir: "{{app}}"; Flags: ignoreversion

Source: "..\\release\\{EXECUTABLE_NAME}_{VERSION}\\VERSAO.txt"; DestDir: "{{app}}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"

Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "Executar {{#MyAppName}}"; Flags: nowait postinstall skipifsilent
"""

    ARQUIVO_ISS.write_text(
        conteudo.strip(),
        encoding="utf-8"
    )

    print(
        f"[OK] Script do instalador gerado: "
        f"{ARQUIVO_ISS}"
    )

    return ARQUIVO_ISS


# ==================================
# COMPILAR INSTALADOR
# ==================================

def compilar_instalador(
    arquivo_iss
):
    caminho_inno_setup = (
        localizar_inno_setup()
    )

    print(
        "[INFO] Inno Setup encontrado:"
    )

    print(
        caminho_inno_setup
    )

    print(
        "[INFO] Gerando instalador..."
    )

    subprocess.run(
        [
            str(caminho_inno_setup),
            str(arquivo_iss)
        ],
        cwd=PASTA_PROJETO,
        check=True
    )

    instalador = (
        PASTA_INSTALLER_OUTPUT
        / f"Automacao_ITI_Setup_{VERSION}.exe"
    )

    if not instalador.exists():
        raise FileNotFoundError(
            "A compilação terminou, mas "
            "o instalador não foi encontrado."
        )

    print(
        f"[OK] Instalador criado: {instalador}"
    )

    return instalador


# ==================================
# RESUMO
# ==================================

def mostrar_resumo(
    executavel,
    pasta_release,
    instalador
):
    tamanho_exe = (
        executavel.stat().st_size
        / 1024
        / 1024
    )

    tamanho_instalador = (
        instalador.stat().st_size
        / 1024
        / 1024
    )

    print()

    print(
        "=" * 65
    )

    print(
        " BUILD CONCLUÍDO COM SUCESSO"
    )

    print(
        "=" * 65
    )

    print(
        f"Aplicação: {APP_NAME}"
    )

    print(
        f"Versão: {VERSION}"
    )

    print()

    print(
        f"Executável:\n{executavel}"
    )

    print(
        f"Tamanho do executável: "
        f"{tamanho_exe:.2f} MB"
    )

    print()

    print(
        f"Release:\n{pasta_release}"
    )

    print()

    print(
        f"Instalador:\n{instalador}"
    )

    print(
        f"Tamanho do instalador: "
        f"{tamanho_instalador:.2f} MB"
    )

    print()

    print(
        "=" * 65
    )


# ==================================
# MAIN
# ==================================

def main():
    print()

    print(
        "=" * 65
    )

    print(
        f" BUILD - {APP_NAME}"
    )

    print(
        f" VERSÃO - {VERSION}"
    )

    print(
        "=" * 65
    )

    print()

    try:
        # 1
        verificar_arquivos()

        # 2
        limpar_build_anterior()

        # 3
        gerar_version_info()

        # 4
        executavel = (
            executar_pyinstaller()
        )

        # 5
        pasta_release = (
            criar_release(
                executavel
            )
        )

        # 6
        arquivo_iss = (
            gerar_script_instalador()
        )

        # 7
        instalador = (
            compilar_instalador(
                arquivo_iss
            )
        )

        # 8
        mostrar_resumo(
            executavel,
            pasta_release,
            instalador
        )

    except subprocess.CalledProcessError as erro:
        print()

        print(
            "[ERRO] Falha ao executar "
            "um programa externo."
        )

        print(
            f"Código de saída: "
            f"{erro.returncode}"
        )

        sys.exit(1)

    except Exception as erro:
        print()

        print(
            "=" * 65
        )

        print(
            " ERRO DURANTE O BUILD"
        )

        print(
            "=" * 65
        )

        print()

        print(
            str(erro)
        )

        print()

        sys.exit(1)


if __name__ == "__main__":
    main()