(use-modules (guix packages)
	(guix gexp)
	((guix licenses) #:prefix license:)
	(guix build-system python)
	(gnu packages python-web)
	(gnu packages node))

(package
	(name "StreamFinder")
	(version "0.0")
	(inputs
		`(("python-flask" ,python-flask)
		  ("python-flask-login" ,python-flask-login)))
	(propagated-inputs '())
	(source (local-file "./src" #:recursive? #t))
	(synopsis "StreamFinder: find what and where to watch!")
	(description
		"StreamFinder allows users to find the movies they want to watch and where they want to watch them.")
	(home-page "https://github.com/Adams475/Streaming-Service-Finder")
	(license license:agpl3+))

