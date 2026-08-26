; YVP Clipper — Windows installer (Inno Setup)
; Build: windows\build-installer.bat (requires ISCC on PATH)

#define MyAppName "YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
#define MyAppExe "YVPClipper.exe"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "NeyroslopInzh"
#define MyAppURL "https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV"

[Setup]
AppId={{B4E8F2A1-9C3D-4E5F-A6B7-8D9E0F1A2B3C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={localappdata}\YVPClipper
DisableDirPage=yes
DisableProgramGroupPage=yes
OutputDir=..\dist\windows
OutputBaseFilename=YVPClipper-Setup
SetupIconFile=..\assets\app.ico
UninstallDisplayIcon={app}\{#MyAppExe}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[CustomMessages]
english.ExtensionHint=After install, open the app once — it will show where the browser extension folder is (Load unpacked).
russian.ExtensionHint=После установки запустите приложение — оно покажет путь к папке расширения (Загрузить распакованное).

[Files]
Source: "..\dist\windows\YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe"; DestDir: "{app}"; DestName: "{#MyAppExe}"; Flags: ignoreversion
Source: "..\extension\manifest.json"; DestDir: "{app}\extension"; Flags: ignoreversion
Source: "..\extension\*.js"; DestDir: "{app}\extension"; Flags: ignoreversion
Source: "..\extension\*.html"; DestDir: "{app}\extension"; Flags: ignoreversion
Source: "..\extension\*.css"; DestDir: "{app}\extension"; Flags: ignoreversion
Source: "..\extension\icons\*"; DestDir: "{app}\extension\icons"; Flags: ignoreversion recursesubdirs

[Registry]
Root: HKCU; Subkey: "Software\Classes\yvp"; ValueType: string; ValueName: ""; ValueData: "URL:YVP Clipper Protocol"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\yvp"; ValueType: string; ValueName: "URL Protocol"; ValueData: ""; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\yvp\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExe},0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\yvp\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExe}"" ""%1"""; Flags: uninsdeletekey

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    SaveStringToFile(ExpandConstant('{app}\.yvp_installed'), '1', False);
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    WizardForm.FinishedLabel.Caption := WizardForm.FinishedLabel.Caption + #13#10#13#10 +
      ExpandConstant('{cm:ExtensionHint}');
  end;
end;
