import jenkins.model.Jenkins
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
import java.nio.file.Files

def changePassword = { username, new_password ->
    def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
        com.cloudbees.plugins.credentials.common.StandardUsernameCredentials.class,
        Jenkins.instance
    )

    def c = creds.findResult { it.username == username ? it : null }

    if ( c ) {
        println "found credential ${c.id} for username ${c.username}"

        def credentials_store = Jenkins.instance.getExtensionList(
            'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
            )[0].getStore()

        def result = credentials_store.updateCredentials(
            com.cloudbees.plugins.credentials.domains.Domain.global(), 
            c, 
            new UsernamePasswordCredentialsImpl(c.scope, c.id, c.description, c.username, new_password)
            )

        if (result) {
            println "password changed for ${username}" 
        } else {
            println "failed to change password for ${username}"
        }
    } else {
      println "could not find credential for ${username}"
    }
}

def envVars = Jenkins.get().getGlobalNodeProperties()[0].getEnvVars()
def username = envVars['JENKINS_USERNAME']

def keyFile = new java.io.File('/run/secrets/jenkins_admin_password')
def key = Files.readString(keyFile.toPath())

changePassword(username, key)
