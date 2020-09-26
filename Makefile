.include <name.py>

SYSPKG = YES
USE_FREENIT = YES
SERVICE != echo ${app_name}
REGGAE_PATH := /usr/local/share/reggae
PORTS = 9000

.include <${REGGAE_PATH}/mk/service.mk>
