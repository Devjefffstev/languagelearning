(defproject lein_dependcy_project "0.1.0-SNAPSHOT"
  :description "Jeff lein project template dependency"
  ;; :dependencies [[org.clojure/clojure "1.11.1"]]
  ;; :repl-options {:init-ns lein-template-project.core}
  :plugins [[com.holychao/parallel-test "0.3.2"]]
  :source-paths ["src/main/clojure"
                 "src/main/resources"]
  :test-paths ["src/test/clojure" "src/test/java" "target/generated-resources"])