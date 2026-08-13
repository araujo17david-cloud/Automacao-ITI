#define MyAppName "Automação ITI"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "INCD"
#define MyAppExeName "Automacao_ITI.exe"

[Setup]
AppId={{7D24F361-7FA9-4A32-A364-ITI2026AUTO}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Automacao ITI
DefaultGroupName=Automação ITI

OutputDir=..\installer_output
OutputBaseFilename=Automacao_ITI_Setup_{#MyAppVersion}

SetupIconFile=..\assets\logo.ico

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=admin

UninstallDisplayIcon={app}\{#MyAppExeName}

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible


[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"


[Files]
Source: "..\release\Automacao_ITI_2.1.0\Automacao_ITI.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "..\release\Automacao_ITI_2.1.0\LEIA-ME.txt"; DestDir: "{app}"; Flags: ignoreversion

Source: "..\release\Automacao_ITI_2.1.0\VERSAO.txt"; DestDir: "{app}"; Flags: ignoreversion


[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked


[Icons]
Name: "{group}\Automação ITI"; Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\Automação ITI"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon


[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar Automação ITI"; Flags: nowait postinstall skipifsilent