CWD=$(shell pwd)

NODE=$(CWD)/node_modules


NPM_PACKAGES_JS = \
	$(NODE)/jquery/dist/jquery \
	$(NODE)/vue/dist/vue

npm:
	npm install

dev: npm clean
	for PKGE in $(NPM_PACKAGES_JS); do \
		ln -sv $$PKGE.js $$PKGE.link.js ; \
	done

prod: npm clean
	for PKGE in $(NPM_PACKAGES_JS); do \
		ln -sv $$PKGE.min.js $$PKGE.link.js ; \
	done

clean:
	for PKGE in $(NPM_PACKAGES_JS); do \
		rm -v $$PKGE.link.js || true ; \
	done

fclean:
	rm -rfv $(NODE)

re: fclean npm