!define PRODUCT_NAME "Photoselect"
!define PRODUCT_VERSION "1.2.2"
!define PY_VERSION "3.8.5"
!define PY_MAJOR_VERSION "3.8"
!define BITNESS "64"
!define ARCH_TAG ".amd64"
!define INSTALLER_NAME "Photoselect_1.2.2.exe"
!define PRODUCT_ICON "icon.ico"

; Marker file to tell the uninstaller that it's a user installation
!define USER_INSTALL_MARKER _user_install_marker

SetCompressor lzma

!if "${NSIS_PACKEDVERSION}" >= 0x03000000
  Unicode true
  ManifestDPIAware true
!endif

!define MULTIUSER_EXECUTIONLEVEL Highest
!define MULTIUSER_INSTALLMODE_DEFAULT_CURRENTUSER
!define MULTIUSER_MUI
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!define MULTIUSER_INSTALLMODE_INSTDIR "Photoselect"
!define MULTIUSER_INSTALLMODE_FUNCTION correct_prog_files
!include MultiUser.nsh
!include FileFunc.nsh

; Modern UI installer stuff
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

; UI pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MULTIUSER_PAGE_INSTALLMODE
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${INSTALLER_NAME}"
ShowInstDetails show

Var cmdLineInstallDir

Section -SETTINGS
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
SectionEnd


Section "!${PRODUCT_NAME}" sec_app
  SetRegView 64
  SectionIn RO
  File ${PRODUCT_ICON}
  SetOutPath "$INSTDIR\pkgs"
  File /r "pkgs\*.*"
  SetOutPath "$INSTDIR"

  ; Marker file for per-user install
  StrCmp $MultiUser.InstallMode CurrentUser 0 +3
    FileOpen $0 "$INSTDIR\${USER_INSTALL_MARKER}" w
    FileClose $0
    SetFileAttributes "$INSTDIR\${USER_INSTALL_MARKER}" HIDDEN

  ; Install files
    SetOutPath "$INSTDIR"
      File "Photoselect.launch.pyw"
      File "icon.ico"
      File "Photoselect_Rename.launch.pyw"
      File "LICENSE"
      File "README.md"

  ; Install directories
    SetOutPath "$INSTDIR\Python"
    File /r "Python\*.*"
    SetOutPath "$INSTDIR\lib"
    File /r "lib\*.*"

  ; Install shortcuts
  ; The output path becomes the working directory for shortcuts
  SetOutPath "%HOMEDRIVE%\%HOMEPATH%"
    CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
    CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Photoselect.lnk" "$INSTDIR\Python\pythonw.exe" \
      '"$INSTDIR\Photoselect.launch.pyw"' "$INSTDIR\icon.ico"
  SetOutPath "$INSTDIR"


  ; Byte-compile Python files.
  DetailPrint "Byte-compiling Python modules..."
  nsExec::ExecToLog '"$INSTDIR\Python\python" -m compileall -q "$INSTDIR\pkgs"'
  WriteUninstaller $INSTDIR\uninstall.exe
  ; Add ourselves to Add/remove programs
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "InstallLocation" "$INSTDIR"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayIcon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                     "Publisher" "Alexander Simunics"
  WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegDWORD SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "NoModify" 1
  WriteRegDWORD SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" \
                   "NoRepair" 1
                    
  ; Add to Directory Background Context menu
  StrCmp $MultiUser.InstallMode CurrentUser 0 +14
    WriteRegStr HKCU "Software\Classes\Directory\shell\${PRODUCT_NAME}" "" "Fotos aussortieren"
    WriteRegStr HKCU "Software\Classes\Directory\shell\${PRODUCT_NAME}" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCU "Software\Classes\Directory\Background\shell\${PRODUCT_NAME}" "" "Fotos aussortieren"
    WriteRegStr HKCU "Software\Classes\Directory\Background\shell\${PRODUCT_NAME}" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCU "Software\Classes\Directory\shell\${PRODUCT_NAME}\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect.launch.pyw" "%1"'
    WriteRegStr HKCU "Software\Classes\Directory\Background\shell\${PRODUCT_NAME}\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect.launch.pyw" "%v"'
    WriteRegStr HKCU "Software\Classes\Directory\shell\${PRODUCT_NAME}_Rename" "" "Fotos umbenennen"
    WriteRegStr HKCU "Software\Classes\Directory\shell\${PRODUCT_NAME}_Rename" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCU "Software\Classes\Directory\Background\shell\${PRODUCT_NAME}_Rename" "" "Fotos umbenennen"
    WriteRegStr HKCU "Software\Classes\Directory\Background\shell\${PRODUCT_NAME}_Rename" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCU "Software\Classes\Directory\shell\${PRODUCT_NAME}_Rename\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect_Rename.launch.pyw" "%1"'
    WriteRegStr HKCU "Software\Classes\Directory\Background\shell\${PRODUCT_NAME}_Rename\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect_Rename.launch.pyw" "%v"'
    Goto contextmenudone
    WriteRegStr HKCR "Directory\shell\${PRODUCT_NAME}" "" "Fotos aussortieren"
    WriteRegStr HKCR "Directory\shell\${PRODUCT_NAME}" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCR "Directory\Background\shell\${PRODUCT_NAME}" "" "Fotos aussortieren"
    WriteRegStr HKCR "Directory\Background\shell\${PRODUCT_NAME}" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCR "Directory\shell\${PRODUCT_NAME}\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect.launch.pyw" "%1"'
    WriteRegStr HKCR "Directory\Background\shell\${PRODUCT_NAME}\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect.launch.pyw" "%v"'
    WriteRegStr HKCR "Directory\shell\${PRODUCT_NAME}_Rename" "" "Fotos umbenennen"
    WriteRegStr HKCR "Directory\shell\${PRODUCT_NAME}_Rename" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCR "Directory\Background\shell\${PRODUCT_NAME}_Rename" "" "Fotos umbenennen"
    WriteRegStr HKCR "Directory\Background\shell\${PRODUCT_NAME}_Rename" "Icon" "$INSTDIR\${PRODUCT_ICON}"
    WriteRegStr HKCR "Directory\shell\${PRODUCT_NAME}_Rename\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect_Rename.launch.pyw" "%1"'
    WriteRegStr HKCR "Directory\Background\shell\${PRODUCT_NAME}_Rename\command" "" '"$INSTDIR\Python\pythonw.exe" "$INSTDIR\Photoselect_Rename.launch.pyw" "%v"'
  contextmenudone:
  

  ; Check if we need to reboot
  IfRebootFlag 0 noreboot
    MessageBox MB_YESNO "A reboot is required to finish the installation. Do you wish to reboot now?" \
                /SD IDNO IDNO noreboot
      Reboot
  noreboot:
SectionEnd

Section "Uninstall"
  SetRegView 64
  SetShellVarContext all
  IfFileExists "$INSTDIR\${USER_INSTALL_MARKER}" 0 +8
    DeleteRegKey HKCU "Software\Classes\Directory\shell\Photoselect"
    DeleteRegKey HKCU "Software\Classes\Directory\Background\shell\Photoselect"
    DeleteRegKey HKCU "Software\Classes\Directory\shell\Photoselect_Rename"
    DeleteRegKey HKCU "Software\Classes\Directory\Background\shell\Photoselect_Rename"
    SetShellVarContext current
    Delete "$INSTDIR\${USER_INSTALL_MARKER}"
    Goto explorerregkeysdone
    DeleteRegKey HKCR "Directory\shell\Photoselect"
    DeleteRegKey HKCR "Directory\Background\shell\Photoselect"
    DeleteRegKey HKCR "Directory\shell\Photoselect_Rename"
    DeleteRegKey HKCR "Directory\Background\shell\Photoselect_Rename"
  explorerregkeysdone:

  Delete $INSTDIR\uninstall.exe
  Delete "$INSTDIR\${PRODUCT_ICON}"
  RMDir /r "$INSTDIR\pkgs"

  ; Remove ourselves from %PATH%

  ; Uninstall files
    Delete "$INSTDIR\Photoselect.launch.pyw"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\Photoselect_Rename.launch.pyw"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\README.md"
  ; Uninstall directories
    RMDir /r "$INSTDIR\Python"
    RMDir /r "$INSTDIR\lib"

  ; Uninstall shortcuts
    RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
  RMDir $INSTDIR
  DeleteRegKey SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
SectionEnd


; Functions

Function .onMouseOverSection
    ; Find which section the mouse is over, and set the corresponding description.
    FindWindow $R0 "#32770" "" $HWNDPARENT
    GetDlgItem $R0 $R0 1043 ; description item (must be added to the UI)

    StrCmp $0 ${sec_app} "" +2
      SendMessage $R0 ${WM_SETTEXT} 0 "STR:${PRODUCT_NAME}"

FunctionEnd

Function .onInit
  ; Multiuser.nsh breaks /D command line parameter. Parse /INSTDIR instead.
  ; Cribbing from https://nsis-dev.github.io/NSIS-Forums/html/t-299280.html
  ${GetParameters} $0
  ClearErrors
  ${GetOptions} '$0' "/INSTDIR=" $1
  IfErrors +2  ; Error means flag not found
    StrCpy $cmdLineInstallDir $1
  ClearErrors

  !insertmacro MULTIUSER_INIT

  ; If cmd line included /INSTDIR, override the install dir set by MultiUser
  StrCmp $cmdLineInstallDir "" +2
    StrCpy $INSTDIR $cmdLineInstallDir
FunctionEnd

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
FunctionEnd

Function correct_prog_files
  ; The multiuser machinery doesn't know about the different Program files
  ; folder for 64-bit applications. Override the install dir it set.
  StrCmp $MultiUser.InstallMode AllUsers 0 +2
    StrCpy $INSTDIR "$PROGRAMFILES64\${MULTIUSER_INSTALLMODE_INSTDIR}"
FunctionEnd
