(defproject lein_template_project "0.1.0-SNAPSHOT"
  :description "Jeff lein project template"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.11.1"]]
  :repl-options {:init-ns lein-template-project.core}
  :plugins [[com.holychao/parallel-test "0.3.2"]])
