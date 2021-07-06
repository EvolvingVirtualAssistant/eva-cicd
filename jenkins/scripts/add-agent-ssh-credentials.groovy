import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.jenkins.plugins.sshcredentials.impl.*
import java.nio.file.Files

def existsCredentialWithId(credentialId) { 
    def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
        BasicSSHUserPrivateKey.class,
        jenkins.model.Jenkins.instance
    )

    def cred = creds.findResult { it.id == credentialId ? it : null }
    println cred
    return cred != null
}

def credentialId = "jenkins"
if(existsCredentialWithId(credentialId)) {
    return String.format("SSH credential with id %s already exists.", credentialId)
}

def keyFile = new java.io.File('/run/secrets/jenkins_eva_agent1_pub_key')
def key = Files.readString(keyFile.toPath())

def source = new BasicSSHUserPrivateKey.DirectEntryPrivateKeySource(key)
def ck1 = new BasicSSHUserPrivateKey(CredentialsScope.GLOBAL, credentialId, "jenkins", source, null, "The eva-jenkins-agent-1 ssh key")

SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), ck1)

return String.format("SSH credential with id %s has been added successfully.", credentialId)