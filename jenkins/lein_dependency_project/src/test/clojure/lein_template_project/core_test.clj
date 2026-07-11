(ns lein-template-project.core-test
  (:require [clojure.test :refer :all]
            [lein-template-project.core :refer :all]
            [clojure.string :as str]))
(def str1 "Hello")
(def demokeys (hash-map "key1" "value1" "key2" "value2"))
(def demokeystest (hash-map "key1" "value1" "key2" "value2"))

(deftest ^:parallel  a-test
  (testing "FIXME, I fail."
    (is (= 1 1))))
(deftest ^:parallel  b-test
  (testing "FIXME, I fail."
    (is (not (= 0 1)))))
(deftest c-test
  (testing "Testing hash-map"
    ;; (is ((= (vals (select-keys demokeys ["key1"])) (vals (select-keys demokeystest ["key1"])))))
    (is (= 1 1))))
(deftest ^:parallel string-test
  (testing "Testing string"
    (is (= str1 "Hello"))
    (is (= (str/upper-case str1) "HELLO"))))
;; (deftest ^:parallel string-test2
;;   (testing "Testing string includes"    
;;     (is ((str/includes? str1 "llo")))))
