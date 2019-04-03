// This is the start of the best framework ever!

node('build-slave') {
    stage 'Build'

    sh "echo command to sync source"
    sh "echo command to build"
}
node('build-slave') {
    stage 'Test'

    sh "echo command to test"
}
