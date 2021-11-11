# relative or absolute path to monitor
PATH_TO_MONITOR = r'C:\Users\sil.comun\Desktop\Compactacao de Solo NB4\Dados Compactacao Solo NB4'

# receivers' emails
RECEIVERS_DANGER = [
    "rodrigo.neto@cnpem.br",
    "matheus.siqueira@cnpem.br",
    "rodrigo.leao@cnpem.br",
    "cassiano.bueno@lnls.br",
    "pedro.martins@cnpem.br"
]
RECEIVERS_ALERT = [
    "rodrigo.neto@cnpem.br"
]

PV_NAME = 'rolo-compressor'

# flag to allow emails to be sent when alert alarms are detected
ALERT_ALARM_ENABLED = True

# acceleration limits to trigger alarm for danger or alert pourposes
LIMITS_DANGER = [0.25, 0.5]
LIMITS_ALERT = [1.2e-3]

# forced delay between sequencial alarms (in seconds)
MINIMUM_TIME_BETWEEN_ALARMS = 0

# mapping between reference in name of files and local of event
REF_MAP = {'CAR': 'Carnauba', 'CAT': 'Caterete'}

# number of neighbor files to save out of the one that triggered an alarm
ADJACENT_FILES_NUMBER = 3
