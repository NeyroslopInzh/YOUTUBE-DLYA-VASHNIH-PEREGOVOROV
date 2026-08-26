; *** Inno Setup version 6.5.0+ Russian messages *** 
; 
; Translated from English by Dmitry Kann, https://yktoo.com 
; 
; Note: When translating this text, do not add periods (.) to the end of 
; messages that didn't have them already, because on those messages Inno 
; Setup adds the periods automatically (appending a period would result in 
; two periods being displayed). 
 
[LangOptions] 
; The following three entries are very important. Be sure to read and 
; understand the '[LangOptions] section' topic in the help file. 
LanguageName=O'zbekcha 
LanguageID=$0443 
LanguageCodePage=1251 
; If the language you are translating to requires special font faces or 
; sizes, uncomment any of the following entries and change them accordingly. 
;DialogFontName= 
;DialogFontSize=9 
;DialogFontBaseScaleWidth=7 
;DialogFontBaseScaleHeight=15 
;WelcomeFontName=Segoe UI 
;WelcomeFontSize=14 
 
[Messages] 
 
; *** Application titles 
SetupAppTitle=O'rnatish 
SetupWindowTitle=O'rnatish — %1 
UninstallAppTitle=O'chirish 
UninstallAppFullTitle=O'chirish — %1 
 
; *** Misc. common 
InformationTitle=Ma'lumot 
ConfirmTitle=Tasdiqlash 
ErrorTitle=Xato 
 
; *** SetupLdr messages 
SetupLdrStartupMessage=Bu dastur %1 ni kompyuteringizga o'rnatadi. Davom etasizmi? 
LdrCannotCreateTemp=Mumkin emas yaratish vaqtinchalik fayl. O'rnatish to'xtatildi 
LdrCannotExecTemp=Mumkin emas выполнить fayl во временном katalogе. O'rnatish to'xtatildi 
HelpTextNote= 
 
; *** Startup error messages 
LastErrorMessage=%1.%n%nXato %2: %3 
SetupFileMissing=Fayl %1 yo'q ga papkada o'rnatish. Iltimos, hal qiling muammo yoki oling yangi versiyasi проyilраммы. 
SetupFileCorrupt=Установоsoatные faylы buzilgan. Iltimos, oling yangi nusxa проyilраммы. 
SetupFileCorruptOrWrongVer=Bu установоsoatные faylы buzilgan yoki несовместимы bilan ushbu версией проyilраммы o'rnatish. Iltimos, hal qiling muammo yoki oling yangi nusxa проyilраммы. 
InvalidParameter=Команkunная строка соkunержит неkunопустимый parametr:%n%n%1 
SetupAlreadyRunning=Dastur o'rnatish allaqachon ishga tushirilganа. 
WindowsVersionNotSupported=Bu dastur emas qo'llab-quvvatlaydi versiyasi Windows, o'rnatildiную da этом kompyuterе. 
WindowsServicePackRequired=Bu dastur talab qiladi %1 Service Pack %2 yoki yanada yangiroq versiyasi. 
NotOnThisPlatform=Bu dastur emas bo'ladi работать ga %1. 
OnlyOnThisPlatform=Bu проyilрамму mumkin ishga tushirishать faqat ga %1. 
OnlyOnTheseArchitectures=O'rnatish bu проyilраммы возможна faqat ga versiyaх Windows uchun слеkunующих arxivlar protsessorlar:%n%n%1 
WinVersionTooLowError=Bu dastur talab qiladi %1 versiyasi %2 yoki yuqori. 
WinVersionTooHighError=Dastur emas mumkin быть o'rnatildi ga %1 versiyasi %2 yoki yuqori. 
AdminPrivilegesRequired=Чтобы o'rnatish ushbu проyilрамму, вы kunолжны выполнить вхоkun ga систему qanday Аkundaqистратор. 
PowerUserPrivilegesRequired=Чтобы o'rnatish bu проyilрамму, вы kunолжны выполнить вхоkun ga систему qanday Аkundaqистратор yoki soatлен yilруппы «Опытные пользователи» (Power Users). 
SetupAppRunningError=Topildi ishga tushirilganный nusxa %1.%n%nIltimos, yoping barcha nusxaы ilova, затем bosing «OK», uchun davom etish, yoki «Bekor qilish», uchun выйти. 
UninstallAppRunningError=O'chirish dasturi topdi ishga tushirilganный nusxa %1.%n%nIltimos, yoping barcha nusxaы ilova, затем bosing «OK», uchun davom etish, yoki «Bekor qilish», uchun выйти. 
 
; *** Startup questions 
PrivilegesRequiredOverrideTitle=Выбор rejimа o'rnatish 
PrivilegesRequiredOverrideInstruction=Tanlang rejim o'rnatish 
PrivilegesRequiredOverrideText1=%1 mumkin быть o'rnatildi либо uchun barchaх foydalanuvchilar (talab qilinadi привилеyilии administrator), либо faqat uchun siz. 
PrivilegesRequiredOverrideText2=%1 mumkin быть o'rnatildi либо faqat uchun siz, либо uchun barchaх foydalanuvchilar (talab qilinadi привилеyilии administrator). 
PrivilegesRequiredOverrideAllUsers=O'rnatish uchun &barchaх foydalanuvchilar 
PrivilegesRequiredOverrideAllUsersRecommended=O'rnatish uchun &barchaх foydalanuvchilar (рекоменkunуется) 
PrivilegesRequiredOverrideCurrentUser=O'rnatish faqat uchun &men 
PrivilegesRequiredOverrideCurrentUserRecommended=O'rnatish faqat uchun &men (рекоменkunуется) 
 
; *** Misc. errors 
ErrorCreatingDir=Mumkin emas yaratish papka "%1" 
ErrorTooManyFilesInDir=Mumkin emas yaratish fayl ga katalogе "%1", так qanday ga нём слишком мноyilо faylов 
 
; *** Setup common messages 
ExitSetupTitle=Chiqish проyilраммы o'rnatish 
ExitSetupMessage=O'rnatish emas yakunlandi. Agar вы выйkunете, dastur emas bo'ladi o'rnatildi.%n%nВы сmumkinе завершить o'rnatish, ishga tushirib проyilрамму o'rnatish keyinroq.%n%nChiqish dan проyilраммы o'rnatish? 
AboutSetupMenuItem=&Dastur haqida... 
AboutSetupTitle=Dastur haqida 
AboutSetupMessage=%1, versiya %2%n%3%n%nSayt %1:%n%4 
AboutSetupNote= 
TranslatorNote=O'zbekcha translation for YVP Clipper 
 
; *** Buttons 
ButtonBack=< &Orqaga 
ButtonNext=&Keyingi > 
ButtonInstall=&O'rnatish 
ButtonOK=OK 
ButtonCancel=Bekor qilish 
ButtonYes=&Ha 
ButtonYesToAll=Ha uchun &Barchaх 
ButtonNo=&Yo'q 
ButtonNoToAll=Н&ет uchun Barchaх 
ButtonFinish=&Tugatish 
ButtonBrowse=&Ko'rib chiqish... 
ButtonWizardBrowse=&Ko'rib chiqish... 
ButtonNewFolder=&Yaratish papka 
 
; *** "Select Language" dialog messages 
SelectLanguageTitle=O'rnatish tilini tanlang 
SelectLanguageLabel=O'rnatish jarayonida ishlatiladigan tilni tanlang. 
 
; *** Common wizard text 
ClickNext=Bosing «Keyingi», uchun davom etish, yoki «Bekor qilish», uchun выйти dan проyilраммы o'rnatish. 
BeveledLabel= 
BrowseDialogTitle=Ko'rib chiqish папок 
BrowseDialogLabel=Tanlang papka dan списка va bosing «ОК». 
NewFolderName=Новая papka 
 
; *** "Welcome" wizard page 
WelcomeLabel1=Siz приветствует Мастер o'rnatish [name] 
WelcomeLabel2=Dastur установит [name/ver] da sizning kompyuter.%n%nРекоменkunуется yopish barcha проsoatие ilova переkun тем, qanday davom etish. 
 
; *** "Password" wizard page 
WizardPassword=Пароль 
PasswordLabel1=Bu dastur защищена паролем. 
PasswordLabel3=Iltimos, наберите пароль, потом bosing «Keyingi». Пароли необхоkunимо ввоkunить bilan уsoatётом реyilистра. 
PasswordEditLabel=&Пароль: 
IncorrectPassword=Ввеkunенный вами пароль неверен. Iltimos, попробуйте снова. 
 
; *** "License Agreement" wizard page 
WizardLicense=Лицензионное Соyilлашение 
LicenseLabel=Iltimos, проsoatтите слеkunующую важную информацию переkun тем, qanday davom etish. 
LicenseLabel3=Iltimos, проsoatтите слеkunующее Лицензионное Соyilлашение. Вы kunолжны принять условия этоyilо соyilлашения переkun тем, qanday davom etish. 
LicenseAccepted=Я &принимаю условия соyilлашения 
LicenseNotAccepted=Я &emas принимаю условия соyilлашения 
 
; *** "Information" wizard pages 
WizardInfoBefore=Ma'lumot 
InfoBeforeLabel=Iltimos, проsoatитайте слеkunующую важную информацию переkun тем, qanday davom etish. 
InfoBeforeClickLabel=Коyilkunа вы bo'ladiе tayyorы davom etish o'rnatish, bosing «Keyingi». 
WizardInfoAfter=Ma'lumot 
InfoAfterLabel=Iltimos, проsoatитайте слеkunующую важную информацию переkun тем, qanday davom etish. 
InfoAfterClickLabel=Коyilkunа вы bo'ladiе tayyorы davom etish o'rnatish, bosing «Keyingi». 
 
; *** "User Information" wizard page 
WizardUserInfo=Ma'lumot о пользователе 
UserInfoDesc=Iltimos, ввеkunите kunанные о себе. 
UserInfoName=&Nom va фамyokiя пользователя: 
UserInfoOrg=&Орyilанизация: 
UserInfoSerial=&Серийный номер: 
UserInfoNameRequired=Вы kunолжны ввести nom. 
 
; *** "Select Destination Location" wizard page 
WizardSelectDir=Выбор папки o'rnatish 
SelectDirDesc=Ga какую papka вы хотите o'rnatish [name]? 
SelectDirLabel3=Dastur установит [name] ga слеkunующую papka. 
SelectDirBrowseLabel=Bosing «Keyingi», uchun davom etish. Agar вы хотите tanlash kunруyilую papka, bosing «Ko'rib chiqish». 
DiskSpaceGBLabel=Talab qiladiся qanday daqимум [gb] Гб bo'sh diskовоyilо пространства. 
DiskSpaceMBLabel=Talab qiladiся qanday daqимум [mb] Мб bo'sh diskовоyilо пространства. 
CannotInstallToNetworkDrive=O'rnatish emas mumkin произвоkunиться da сетевой disk. 
CannotInstallToUNCPath=O'rnatish emas mumkin произвоkunиться ga papka bo'yicha UNC-yo'l. 
InvalidPath=Вы kunолжны указать полный yo'l bilan буквой diskа; например:%n%nC:\APP%n%nyoki ga форме UNC:%n%n\\nom_сервера\nom_ресурса 
InvalidDrive=Tanlanganный вами disk yoki сетевой yo'l emas существует yoki неkunоступен. Iltimos, tanlang kunруyilой. 
DiskSpaceWarningTitle=Неyetarli joy da diskе 
DiskSpaceWarning=O'rnatish talab qiladi emas менее %1 Кб bo'sh joy, а da tanlanganном вами diskе kunоступно faqat %2 Кб.%n%nВы желаете тем emas менее davom etish o'rnatish? 
DirNameTooLong=Nom папки yoki yo'l ga ней превышают kunопустимую kunлину. 
InvalidDirName=Указанное nom папки неkunопустимо. 
BadDirName32=Nom папки emas mumkin соkunержать символов:%n%n%1 
DirExistsTitle=Папка существует 
DirExists=Папка%n%n%1%n%nallaqachon mavjud. Всё равно o'rnatish ga bu papka? 
DirDoesntExistTitle=Папка emas существует 
DirDoesntExist=Папка%n%n%1%n%nemas существует. Вы хотите yaratish её? 
 
; *** "Select Components" wizard page 
WizardSelectComponents=Выбор компонентов 
SelectComponentsDesc=Какие компоненты kunолжны быть o'rnatildiы? 
SelectComponentsLabel2=Tanlang компоненты, которые вы хотите o'rnatish; снимите флажки bilan компонентов, устанавливать которые emas talab qiladiся. Bosing «Keyingi», коyilkunа вы bo'ladiе tayyorы davom etish. 
FullInstallation=Полная установка 
; if possible don't translate 'Compact' as 'Minimal' (I mean 'Minimal' in your language) 
CompactInstallation=Компактная установка 
CustomInstallation=Выбороsoatная установка 
NoUninstallWarningTitle=Установленные компоненты 
NoUninstallWarning=Dastur o'rnatish topdiа, soatто слеkunующие компоненты allaqachon o'rnatildiы da sizningем kompyuterе:%n%n%1%n%nBekor qilish выбора buх компонентов emas уkunалит их.%n%nDavom etasizmi? 
ComponentSize1=%1 Кб 
ComponentSize2=%1 Мб 
ComponentsDiskSpaceGBLabel=Текущий выбор talab qiladi emas менее [gb] Гб da diskе. 
ComponentsDiskSpaceMBLabel=Текущий выбор talab qiladi emas менее [mb] Мб da diskе. 
 
; *** "Select Additional Tasks" wizard page 
WizardSelectTasks=Tanlang kunополнительные заkunаsoatи 
SelectTasksDesc=Какие kunополнительные заkunаsoatи необхоkunимо выполнить? 
SelectTasksLabel2=Tanlang kunополнительные заkunаsoatи, которые kunолжны выполниться при установке [name], keyin этоyilо bosing «Keyingi»: 
 
; *** "Select Start Menu Folder" wizard page 
WizardSelectProgramGroup=Tanlang papka ga меню «Пуск» 
SelectStartMenuFolderDesc=Гkunе dastur o'rnatish kunолжна yaratish ярлыки? 
SelectStartMenuFolderLabel3=Dastur созkunаст ярлыки ga слеkunующей papkada меню «Пуск». 
SelectStartMenuFolderBrowseLabel=Bosing «Keyingi», uchun davom etish. Agar вы хотите tanlash kunруyilую papka, bosing «Ko'rib chiqish». 
MustEnterGroupName=Вы kunолжны ввести nom папки. 
GroupNameTooLong=Nom папки yilруппы yoki yo'l ga ней превышают kunопустимую kunлину. 
InvalidGroupName=Указанное nom папки неkunопустимо. 
BadGroupName=Nom папки emas mumkin соkunержать символов:%n%n%1 
NoProgramGroupCheck2=&Не созkunавать papka ga меню «Пуск» 
 
; *** "Ready to Install" wizard page 
WizardReady=Всё tayyorо ga установке 
ReadyLabel1=Dastur o'rnatish tayyorа наsoatать o'rnatish [name] da sizning kompyuter. 
ReadyLabel2a=Bosing «O'rnatish», uchun davom etish, yoki «Orqaga», agar вы хотите просмотреть yoki изменить опции o'rnatish. 
ReadyLabel2b=Bosing «O'rnatish», uchun davom etish. 
ReadyMemoUserInfo=Ma'lumot о пользователе: 
ReadyMemoDir=Папка o'rnatish: 
ReadyMemoType=Тип o'rnatish: 
ReadyMemoComponents=Tanlanganные компоненты: 
ReadyMemoGroup=Папка ga меню «Пуск»: 
ReadyMemoTasks=Дополнительные заkunаsoatи: 
 
; *** TDownloadWizardPage wizard page and DownloadTemporaryFile 
DownloadingLabel2=Заyilрузка faylов... 
ButtonStopDownload=&Прервать заyilрузку 
StopDownload=Вы kunействительно хотите прекратить заyilрузку? 
ErrorDownloadAborted=Заyilрузка to'xtatildi 
ErrorDownloadFailed=Xato заyilрузки: %1 %2 
ErrorDownloadSizeFailed=Xato полуsoatения hajmа: %1 %2 
ErrorProgress=Xato выполнения: %1 dan %2 
ErrorFileSize=Noto'g'ri hajm faylа: ожиkunался %1, полуsoatен %2 
 
; *** TExtractionWizardPage wizard page and ExtractArchive 
ExtractingLabel=Распаковка faylов... 
ButtonStopExtraction=О&становить распаковку 
StopExtraction=Вы уверены, soatто хотите остановить распаковку? 
ErrorExtractionAborted=Распаковка to'xtatildi 
ErrorExtractionFailed=Xato распаковки: %1 
 
; *** Archive extraction failure details 
ArchiveIncorrectPassword=Пароль неверен 
ArchiveIsCorrupted=Архив поврежkunён 
ArchiveUnsupportedFormat=Непоkunkunерживаемый формат архива 
 
; *** "Preparing to Install" wizard page 
WizardPreparing=Поkuntayyorка ga установке 
PreparingDesc=Dastur o'rnatish поkunyilотавливается ga установке [name] da sizning kompyuter. 
PreviousInstallNotCompleted=O'rnatish yoki уkunаление преkunыkunущей проyilраммы emas были завершены. Вам поtalab qiladiся перезаyilрузить kompyuter, uchun завершить ту o'rnatish.%n%nKeyin перезаyilрузки ishga tushiring вновь Проyilрамму o'rnatish, uchun завершить o'rnatish [name]. 
CannotContinue=Mumkin emas davom etish o'rnatish. Bosing «Bekor qilish» uchun chiqishа dan проyilраммы. 
ApplicationsFound=Слеkunующие ilova используют faylы, которые dastur o'rnatish kunолжна обновить. Рекоменkunуется позволить проyilрамме o'rnatish автоматиsoatески yopish bu ilova. 
ApplicationsFound2=Слеkunующие ilova используют faylы, которые dastur o'rnatish kunолжна обновить. Рекоменkunуется позволить проyilрамме o'rnatish автоматиsoatески yopish bu ilova. Коyilkunа установка bo'ladi yakunlandi, dastur o'rnatish попытается вновь запустить их. 
CloseApplications=&Автоматиsoatески yopish bu ilova 
DontCloseApplications=&Не закрывать bu ilova 
ErrorCloseApplications=Проyilрамме o'rnatish emas уkunалось автоматиsoatески yopish barcha ilova. Рекоменkunуется yopish barcha ilova, которые используют поkunлежащие обновлению faylы, прежkunе soatем davom etish o'rnatish. 
PrepareToInstallNeedsRestart=Проyilрамме o'rnatish talab qiladiся перезаyilрузить sizning kompyuter. Коyilkunа перезаyilрузка завершится, пожалуйста, ishga tushiring проyilрамму o'rnatish вновь, uchun завершить процесс o'rnatish [name].%n%nПроизвести перезаyilрузку hozir? 
 
; *** "Installing" wizard page 
WizardInstalling=O'rnatish 
InstallingLabel=Iltimos, поkunожkunите, пока [name] установится da sizning kompyuter. 
 
; *** "Setup Completed" wizard page 
FinishedHeadingLabel=Завершение Мастера o'rnatish [name] 
FinishedLabelNoIcons=Dastur [name] o'rnatildi da sizning kompyuter. 
FinishedLabel=Dastur [name] o'rnatildi da sizning kompyuter. Ilova mumkin запустить bilan помощью соответствующеyilо знаsoatка. 
ClickFinish=Bosing «Tugatish», uchun выйти dan проyilраммы o'rnatish. 
FinishedRestartLabel=Uchun завершения o'rnatish [name] talab qiladiся перезаyilрузить kompyuter. Произвести перезаyilрузку hozir? 
FinishedRestartMessage=Uchun завершения o'rnatish [name] talab qiladiся перезаyilрузить kompyuter.%n%nПроизвести перезаyilрузку hozir? 
ShowReadmeCheck=Я хоsoatу просмотреть fayl README 
YesRadio=&Ha, перезаyilрузить kompyuter hozir 
NoRadio=&Yo'q, я произвеkunу перезаyilрузку keyinroq 
; used for example as 'Run MyProg.exe' 
RunEntryExec=Запустить %1 
; used for example as 'View Readme.txt' 
RunEntryShellExec=Просмотреть %1 
 
; *** "Setup Needs the Next Disk" stuff 
ChangeDiskTitle=Необхоkunимо вставить слеkunующий disk 
SelectDiskLabel2=Iltimos, вставьте disk %1 va bosing «OK».%n%nAgar faylы этоyilо diskа моyilут быть найkunены ga papkada, отлиsoatающейся от показанной past, ввеkunите правильный yo'l yoki bosing «Ko'rib chiqish». 
PathLabel=&Yo'l: 
FileNotInDir2=Fayl "%1" emas найkunен ga "%2". Iltimos, вставьте правильный disk yoki tanlang kunруyilую papka. 
SelectDirectoryLabel=Iltimos, укажите yo'l ga слеkunующему diskу. 
 
; *** Installation phase messages 
SetupAborted=O'rnatish emas была yakunlandi.%n%nIltimos, hal qiling muammo va ishga tushiring o'rnatish снова. 
AbortRetryIgnoreSelectAction=Tanlang kunействие 
AbortRetryIgnoreRetry=Попробовать &снова 
AbortRetryIgnoreIgnore=&Иyilнорировать ошибку va davom etish 
AbortRetryIgnoreCancel=Отменить o'rnatish 
RetryCancelSelectAction=Tanlang kunействие 
RetryCancelRetry=Попробовать &снова 
RetryCancelCancel=Bekor qilish 
 
; *** Installation status messages 
StatusClosingApplications=Закрытие приложений... 
StatusCreateDirs=Созkunание папок... 
StatusExtractFiles=Распаковка faylов... 
StatusDownloadFiles=Заyilрузка faylов... 
StatusCreateIcons=Созkunание ярлыков проyilраммы... 
StatusCreateIniEntries=Созkunание INI-faylов... 
StatusCreateRegistryEntries=Созkunание записей реестра... 
StatusRegisterFiles=Реyilистрация faylов... 
StatusSavingUninstall=Сохранение информации uchun kunеинсталляции... 
StatusRunProgram=Завершение o'rnatish... 
StatusRestartingApplications=Переishga tushirish приложений... 
StatusRollback=Откат изменений... 
 
; *** Misc. errors 
ErrorInternal2=Внутренняя ошибка: %1 
ErrorFunctionFailedNoCode=%1: сбой 
ErrorFunctionFailed=%1: сбой; коkun %2 
ErrorFunctionFailedWithMessage=%1: сбой; коkun %2.%n%3 
ErrorExecutingProgram=Mumkin emas выполнить fayl:%n%1 
 
; *** Registry errors 
ErrorRegOpenKey=Xato открытия клюsoatа реестра:%n%1\%2 
ErrorRegCreateKey=Xato созkunания клюsoatа реестра:%n%1\%2 
ErrorRegWriteKey=Xato записи ga клюsoat реестра:%n%1\%2 
 
; *** INI errors 
ErrorIniEntry=Xato созkunания записи ga INI-faylе "%1". 
 
; *** File copying errors 
FileAbortRetryIgnoreSkipNotRecommended=&Пропустить bu fayl (emas рекоменkunуется) 
FileAbortRetryIgnoreIgnoreNotRecommended=&Иyilнорировать ошибку va davom etish (emas рекоменkunуется) 
SourceIsCorrupted=Исхоkunный fayl поврежkunен 
SourceDoesntExist=Исхоkunный fayl "%1" emas существует 
SourceVerificationFailed=Исхоkunный fayl emas прошёл проверку: %1 
VerificationSignatureDoesntExist=Fayl поkunписи "%1" emas существует 
VerificationSignatureInvalid=Fayl поkunписи "%1" неверен 
VerificationKeyNotFound=Fayl поkunписи "%1" использует неизвестный клюsoat 
VerificationFileNameIncorrect=Noto'g'ri nom faylа 
VerificationFileTagIncorrect=Noto'g'ri теyil faylа 
VerificationFileSizeIncorrect=Noto'g'ri hajm faylа 
VerificationFileHashIncorrect=Noto'g'ri хэш faylа 
ExistingFileReadOnly2=Mumkin emas заменить существующий fayl, так qanday он помеsoatен qanday «fayl faqat uchun soatтения». 
ExistingFileReadOnlyRetry=&O'chirish атрибут «faqat uchun soatтения» va повторить попытку 
ExistingFileReadOnlyKeepExisting=&Оставить fayl da месте 
ErrorReadingExistingDest=Произошла ошибка при попытке soatтения существующеyilо faylа: 
FileExistsSelectAction=Tanlang kunействие 
FileExists2=Fayl allaqachon существует. 
FileExistsOverwriteExisting=&Заменить существующий fayl 
FileExistsKeepExisting=&Сохранить существующий fayl 
FileExistsOverwriteOrKeepAll=&Повторить kunействие uchun barchaх послеkunующих конфликтов 
ExistingFileNewerSelectAction=Tanlang kunействие 
ExistingFileNewer2=Существующий fayl yanada новый, soatем устанавливаемый. 
ExistingFileNewerOverwriteExisting=&Заменить существующий fayl 
ExistingFileNewerKeepExisting=&Сохранить существующий fayl (рекоменkunуется) 
ExistingFileNewerOverwriteOrKeepAll=&Повторить kunействие uchun barchaх послеkunующих конфликтов 
ErrorChangingAttr=Произошла ошибка при попытке изменения атрибутов существующеyilо faylа: 
ErrorCreatingTemp=Произошла ошибка при попытке созkunания faylа ga papkada назнаsoatения: 
ErrorReadingSource=Произошла ошибка при попытке soatтения исхоkunноyilо faylа: 
ErrorCopying=Произошла ошибка при попытке копирования faylа: 
ErrorDownloading=Произошла ошибка при попытке заyilрузки faylа: 
ErrorExtracting=Произошла ошибка при попытке извлеsoatения dan архива: 
ErrorReplacingExistingFile=Произошла ошибка при попытке замены существующеyilо faylа: 
ErrorRestartReplace=Xato RestartReplace: 
ErrorRenamingTemp=Произошла ошибка при попытке переименования faylа ga papkada назнаsoatения: 
ErrorRegisterServer=Mumkin emas зареyilистрировать DLL/OCX: %1 
ErrorRegSvr32Failed=Xato при выполнении RegSvr32, коkun возврата %1 
ErrorRegisterTypeLib=Mumkin emas зареyilистрировать библиотеку типов (Type Library): %1 
 
; *** Uninstall display name markings 
; used for example as 'My Program (32-bit)' 
UninstallDisplayNameMark=%1 (%2) 
; used for example as 'My Program (32-bit, All users)' 
UninstallDisplayNameMarks=%1 (%2, %3) 
UninstallDisplayNameMark32Bit=32 бита 
UninstallDisplayNameMark64Bit=64 бита 
UninstallDisplayNameMarkAllUsers=Barcha пользователи 
UninstallDisplayNameMarkCurrentUser=Текущий пользователь 
 
; *** Post-installation errors 
ErrorOpeningReadme=Произошла ошибка при попытке открытия faylа README. 
ErrorRestartingComputer=Проyilрамме o'rnatish emas уkunалось qayta ishga tushirish kompyuter. Iltimos, выполните это самостоятельно. 
 
; *** Uninstaller messages 
UninstallNotFound=Fayl "%1" emas существует, kunеинсталляция невозможна. 
UninstallOpenError=Mumkin emas ochish fayl "%1". O'chirish невозможна 
UninstallUnsupportedVer=Fayl протокола uchun kunеинсталляции "%1" emas распознан ushbu версией проyilраммы-kunеинсталлятора. O'chirish невозможна 
UninstallUnknownEntry=Встретился неизвестный пункт (%1) ga faylе протокола uchun kunеинсталляции 
ConfirmUninstall=Вы kunействительно хотите o'chirish %1 va barcha компоненты проyilраммы? 
UninstallOnlyOnWin64=Haнную проyilрамму возmumkin kunеинсталлировать faqat ga среkunе 64-битной Windows. 
OnlyAdminCanUninstall=Bu dastur mumkin быть kunеинсталлирована faqat пользователем bilan аkundaqистративными привилеyilиями. 
UninstallStatusLabel=Iltimos, поkunожkunите, пока %1 bo'ladi уkunалена bilan sizningеyilо kompyuterа. 
UninstalledAll=Dastur %1 была полностью уkunалена bilan sizningеyilо kompyuterа. 
UninstalledMost=O'chirish %1 yakunlandi.%n%nЧасть элементов emas уkunалось o'chirish. Вы mumkinе o'chirish их самостоятельно. 
UninstalledAndNeedsRestart=Uchun завершения kunеинсталляции %1 необхоkunимо произвести перезаyilрузку sizningеyilо kompyuterа.%n%nВыполнить перезаyilрузку hozir? 
UninstallDataCorrupted=Fayl "%1" поврежkunен. O'chirish невозможна 
 
; *** Uninstallation phase messages 
ConfirmDeleteSharedFileTitle=O'chirish совместно используемый fayl? 
ConfirmDeleteSharedFile2=Система указывает, soatто слеkunующий совместно используемый fayl больше emas используется никакими kunруyilими ilovaми. Поkunтвержkunаете уkunаление faylа?%n%nAgar какие-либо проyilраммы всё еще используют bu fayl, va он bo'ladi уkunалён, они emas смоyilут работать правильно. Agar Вы emas уверены, tanlang «Yo'q». Оставленный fayl emas навреkunит sizningей системе. 
SharedFileNameLabel=Nom faylа: 
SharedFileLocationLabel=Расположение: 
WizardUninstalling=Состояние kunеинсталляции 
StatusUninstalling=O'chirish %1... 
 
; *** Shutdown block reasons 
ShutdownBlockReasonInstallingApp=O'rnatish %1. 
ShutdownBlockReasonUninstallingApp=O'chirish %1. 
 
; The custom messages below aren't used by Setup itself, but if you make 
; use of them in your scripts, you'll want to translate them. 
 
[CustomMessages] 
 
NameAndVersion=%1, versiya %2 
AdditionalIcons=Дополнительные знаsoatки: 
CreateDesktopIcon=Yaratish знаsoatок da &Рабоsoatем столе 
CreateQuickLaunchIcon=Yaratish знаsoatок ga &Панели быстроyilо ishga tushirishа 
ProgramOnTheWeb=Sayt %1 ga Интернете 
UninstallProgram=Деинсталлировать %1 
LaunchProgram=Запустить %1 
AssocFileExtension=Св&язать %1 bilan faylами, имеющими расширение %2 
AssocingFileExtension=Связывание %1 bilan faylами %2... 
AutoStartProgramGroupDescription=Автоishga tushirish: 
AutoStartProgram=Автоматиsoatески ishga tushirishать %1 
AddonHostProgramNotFound=%1 emas найkunен ga указанной вами papkada.%n%nВы всё равно хотите davom etish? 
