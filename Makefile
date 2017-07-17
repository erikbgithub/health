.PHONY: remove
remove:
	-rm /etc/default/health
	-rm /lib/systemd/system/health.service
	-rm /etc/flask/health.py

.PHONY: install
install: remove
	cp ${CURDIR}/defaults /etc/default/health
	cp ${CURDIR}/health.service /lib/systemd/system/health.service
	mkdir -p /etc/flask
	cp ${CURDIR}/health.py /etc/flask/health.py

.PHONY: run
run: stop
	systemctl enable health.service
	systemctl start health.service
	-systemctl status health.service

.PHONY: stop
stop:
	systemctl disable health.service
	systemctl stop health.service
	-systemctl status health.service

.PHONY: purge
purge: stop remove
