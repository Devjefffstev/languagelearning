(ns lein-template-project.core )

(defn foo
  "I don't do a whole lot."
  [x]
  (println x "Hello, World!"))
(defn examplehash []
  (def demohash (hash-map "z" 1 "b" 2 "a" 3))
  (println (vals (select-keys demohash ["z"]))))

(examplehash)
(foo "Hello")
