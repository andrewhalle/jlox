build:
	mkdir build
	javac -d build src/*.java

gen-ast:
	python tool/generate-ast.py src

clean:
	rm -rf build

run file:
  cd build && java com.andrewhalle.lox.Lox ../{{file}}
