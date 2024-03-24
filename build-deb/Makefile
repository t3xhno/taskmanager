all: man deb 

man: man/taskmanager.1.md
	pandoc man/taskmanager.1.md -f markdown+hard_line_breaks -s -t man -o man/taskmanager.1
	cp man/taskmanager.1 taskmanager/usr/share/man/man1/
	gzip -f taskmanager/usr/share/man/man1/taskmanager.1
deb: man ../requirments.txt ../run.py ../taskmanager ../LICENSE
	cp -r ../taskmanager/* taskmanager/var/taskmanager/taskmanager/
	cp ../run.py taskmanager/var/taskmanager/
	cp ../init_db.py taskmanager/var/taskmanager/
	cp ../LICENSE taskmanager/var/taskmanager/
	chmod -w taskmanager/DEBIAN/*
	chmod +w taskmanager/DEBIAN/control
	dpkg-deb --build taskmanager
	chmod +w taskmanager/DEBIAN/*
clean:
	rm -f taskmanager.deb
	rm -f man/taskmanager.1
	rm -rf taskmanager/var
	mkdir -p taskmanager/var/taskmanager/taskmanager
	mkdir -p taskmanager/usr/share/man/man1/
