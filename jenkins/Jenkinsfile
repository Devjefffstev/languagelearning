#!groovy
// @Library('shared-library') _
// pipeline {
//     agent { label 'maven-node' }
//     tools {
//         maven 'MavenHome'
//         jdk 'JAVAHOME'
//     }
//     stages {
        // stage('Check Linux Version') {
        //     steps {
        //         script {
        //             def linuxVersion = sh(script: 'cat /etc/os-release', returnStdout: true).trim()
        //             echo "Linux Version: ${linuxVersion}"
        //         }
        //     }
        // }
        // stage('clojure') {
        //     steps {
        //         echo 'Clojure version: Hola'
        //     }
        // }
        // stage('using libraries') {
        //     steps {
        //         helloWorld(name: 'Alice', dayOfWeek: 'Monday')
        //     }
        // }
        // stage('Build parallelProject') {
        //     steps {
        //         dir('parallelTestExecutor') {
        //             sh 'mvn clean install'
        //         }
        //     }
        // }
        // stage('Test parallelProject') {
        //     steps {
        //         dir('parallelTestExecutor') {
        //             sh 'mvn test'
        //         }
        //     }
        // }
        // stage('Clone Calculator project') {
        //     steps {
        //             git url: 'https://github.com/Ratnakar14/CalculatorWithSpringBoot.git', branch: 'main'
        //     }
        // }
        // stage('Build Calculator project') {
        //     steps {
        //         dir('calculater/calculater/ASL Coding Test') {
        //             sh 'mvn clean install'
        //         }
        //     }
        // }
        // stage('Test Calculator project') {
        //     steps {
        //         dir('calculater/calculater/ASL Coding Test') {
        //             sh 'mvn test'
        //         }
        //     }
        // }
//         stage('Build CalculatorWithTest project') {
//             steps {
//                 dir('CalculatorWithTest') {
//                     sh 'mvn clean install -DskipTests'
//                 }
//             }
//         }
//         stage('Test CalculatorWithTest project') {
//             steps {
//                 dir('CalculatorWithTest') {
//                     sh 'mvn test'
//                 }
//             }
//         }
//     }
// }

node('maven-node') {
    // Define tools
    def mvnHome = tool name: 'MavenHome', type: 'maven'
    def jdkHome = tool name: 'JAVAHOME', type: 'jdk'

    // Set environment variables
    env.PATH = "${jdkHome}/bin:${mvnHome}/bin:${env.PATH}"
    // Capture the start time
    def startTime = System.currentTimeMillis()
    echo "Pipeline started at: ${new Date(startTime)}"

    stage('check folder') {
        sh 'ls -l'
        echo "Pipeline started at: ${new Date(startTime)}"
    }
    stage('clone repo') {
        // Clone the repository
        git url: 'https://github.com/Devjefffstev/jenkins.git', branch: 'main'
    }
    stage('Build CalculatorWithTest project') {
        dir('CalculatorWithTest') {
            sh 'mvn clean install -DskipTests'
        }
    }

    // stage('Test CalculatorWithTest project') {
    //     dir('CalculatorWithTest') {
    //         sh 'mvn test'
    //     }
    // }

    stage('Parallel Test Execution') {
            sh 'ls -l'
            // Request the test groupings based on previous test results
            def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true

            // Create dictionary to hold set of parallel test executions
            def testGroups = [:]

            for (int i = 0; i < splits.size(); i++) {
                def split = splits[i]

                // Loop over each record in splits to prepare the testGroups that we'll run in parallel
                testGroups["split-${i}"] = {
                    node('maven-node')  {
                        checkout scm
                    dir('CalculatorWithTest') {
                        sh 'ls -l'
                        // Clean each test node to start
                        sh 'mvn clean'

                        def mavenInstall = 'install -Dmaven.test.failure.ignore=true'

                        // Write includesFile or excludesFile for tests
                        if (split.includes) {
                            writeFile file: "target/parallel-test-includes-${i}.txt", text: split.list.join('\n')
                            mavenInstall += " -Dsurefire.includesFile=target/parallel-test-includes-${i}.txt"
 } else {
                            writeFile file: "target/parallel-test-excludes-${i}.txt", text: split.list.join('\n')
                            mavenInstall += " -Dsurefire.excludesFile=target/parallel-test-excludes-${i}.txt"
                        }

                        // Call the Maven build with tests
                        sh "mvn ${mavenInstall}"

                    // Archive the test results
                    // junit '**/target/surefire-reports/TEST-*.xml'
                    }
                    }
                }
            }
            parallel testGroups
    }
    // Capture the end time
    def endTime = System.currentTimeMillis()
    echo "Pipeline ended at: ${new Date(endTime)}"

    // Calculate and display the total duration
    def durationInMinutes = (endTime - startTime) / (1000 * 60)
    def durationInSeconds = (endTime - startTime) / 1000
    echo "Total Pipeline Duration: ${durationInMinutes} minutes"

    stage('Clean Workspace') {
            // Clean the workspace after the build and test stages
            sh 'rm -rf *'
            echo "Pipeline ended at: ${new Date(endTime)}"
            echo "Pipeline Started at: ${startTime}"
            echo "Pipeline Finished at: ${endTime}"
            echo "Total Pipeline Duration: ${durationInMinutes} minutes"
            echo "Total Pipeline Duration: ${durationInSeconds} seconds"
    }
}
