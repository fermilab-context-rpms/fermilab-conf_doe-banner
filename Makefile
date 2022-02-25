_default:
	@echo "make"
sources:
	@echo "make sources"
srpm: sources
	@echo "make srpm"
	rpmbuild -bs --define '_sourcedir .' --define '_srcrpmdir .' fermilab-conf_doe-banner.spec
