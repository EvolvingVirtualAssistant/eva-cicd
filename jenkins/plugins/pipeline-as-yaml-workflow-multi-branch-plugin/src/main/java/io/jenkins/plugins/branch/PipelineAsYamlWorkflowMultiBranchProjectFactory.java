package io.jenkins.plugins.branch;

import edu.umd.cs.findbugs.annotations.NonNull;
import hudson.Extension;
import hudson.model.ItemGroup;
import io.jenkins.plugins.pipeline.PipelineAsYamlWorkflowBranchProjectFactory;
import java.util.Map;
import javax.annotation.CheckForNull;
import javax.annotation.Nonnull;
import jenkins.branch.MultiBranchProject;
import jenkins.branch.MultiBranchProjectFactory;
import jenkins.branch.MultiBranchProjectFactoryDescriptor;
import jenkins.plugins.git.traits.LocalBranchTrait;
import jenkins.scm.api.SCMSource;
import jenkins.scm.api.SCMSourceCriteria;
import org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.stapler.DataBoundSetter;

public class PipelineAsYamlWorkflowMultiBranchProjectFactory extends
    MultiBranchProjectFactory.BySCMSourceCriteria {

    private final static String YAML_JENKINS_FILE = "Jenkinsfile.yaml";

    private String yamlJenkinsFile;

    private ExtendedPipelineAsYamlWorkflowBranchProjectFactory pipelineAsYamlWorkflowBranchProjectFactory;

    private static class ExtendedPipelineAsYamlWorkflowBranchProjectFactory extends
        PipelineAsYamlWorkflowBranchProjectFactory {

        private static String innerYamlJenkinsFile;

        public ExtendedPipelineAsYamlWorkflowBranchProjectFactory(String yamlJenkinsFile) {
            super(yamlJenkinsFile);
        }

        public SCMSourceCriteria getVisibleSCMSourceCriteria(SCMSource source) {
            return getSCMSourceCriteria(source);
        }

        synchronized static void setInnerYamlJenkinsFile(String file) {
            innerYamlJenkinsFile = file;
        }

        @Override
        protected SCMSourceCriteria getSCMSourceCriteria(SCMSource source) {
            this.setYamlJenkinsFile(innerYamlJenkinsFile);
            return super.getSCMSourceCriteria(source);
        }

        @Extension
        public static class DescriptorImpl extends AbstractWorkflowBranchProjectFactoryDescriptor {

            public DescriptorImpl() {
            }

            @Nonnull
            public String getDisplayName() {
                return DescriptorMessages.My_ProjectRecognizer_DisplayName();
            }
        }
    }

    public PipelineAsYamlWorkflowMultiBranchProjectFactory() {
    }

    /**
     * Constructor
     *
     * @param yamlJenkinsFile Path of the Pipeline As Yaml script file in SCM
     */
    @DataBoundConstructor
    public PipelineAsYamlWorkflowMultiBranchProjectFactory(String yamlJenkinsFile) {
        this.yamlJenkinsFile = yamlJenkinsFile;
        ExtendedPipelineAsYamlWorkflowBranchProjectFactory
            .setInnerYamlJenkinsFile(this.yamlJenkinsFile);
        initializePipelineFactoryIfNull(this.yamlJenkinsFile);
        this.pipelineAsYamlWorkflowBranchProjectFactory.setYamlJenkinsFile(this.yamlJenkinsFile);
    }

    @DataBoundSetter
    public void setYamlJenkinsFile(String yamlJenkinsFile) {
        this.yamlJenkinsFile = yamlJenkinsFile;
        ExtendedPipelineAsYamlWorkflowBranchProjectFactory
            .setInnerYamlJenkinsFile(this.yamlJenkinsFile);
        initializePipelineFactoryIfNull(this.yamlJenkinsFile);
        this.pipelineAsYamlWorkflowBranchProjectFactory.setYamlJenkinsFile(this.yamlJenkinsFile);
    }

    @Override
    protected SCMSourceCriteria getSCMSourceCriteria(@NonNull SCMSource source) {
        return newFactory().getPipelineAsYamlWorkflowBranchProjectFactory()
            .getVisibleSCMSourceCriteria(source);
    }

    @NonNull
    @Override
    protected MultiBranchProject<?, ?> doCreateProject(@NonNull ItemGroup<?> parent,
        @NonNull String name, @NonNull Map<String, Object> attributes) {
        initializePipelineFactoryIfNull();
        WorkflowMultiBranchProject project = new WorkflowMultiBranchProject(parent, name);
        project.setProjectFactory(this.pipelineAsYamlWorkflowBranchProjectFactory);

        // For now adding localBranchTrait is being done directly here since the projects are not
        // inheriting the configuration from the organization folder
        final boolean hasLocalBranchTrait = project.getSCMSources().stream()
            .filter(source -> source.getTraits() != null)
            .flatMap(source -> source.getTraits().stream())
            .anyMatch(scmSourceTrait -> scmSourceTrait instanceof LocalBranchTrait);

        if (!hasLocalBranchTrait) {
            project.getSCMSources().stream()
                .filter(source -> source.getTraits() != null)
                .forEach(source -> source.getTraits().add(new LocalBranchTrait()));
        }

        return project;
    }

    public ExtendedPipelineAsYamlWorkflowBranchProjectFactory getPipelineAsYamlWorkflowBranchProjectFactory() {
        return this.pipelineAsYamlWorkflowBranchProjectFactory;
    }

    public PipelineAsYamlWorkflowMultiBranchProjectFactory newFactory() {
        return new PipelineAsYamlWorkflowMultiBranchProjectFactory(this.yamlJenkinsFile);
    }

    @Extension
    public static class DescriptorImpl extends MultiBranchProjectFactoryDescriptor {

        public DescriptorImpl() {
        }

        @CheckForNull
        @Override
        public MultiBranchProjectFactory newInstance() {
            return new PipelineAsYamlWorkflowMultiBranchProjectFactory();
        }

        @Nonnull
        public String getDisplayName() {
            return DescriptorMessages.My_ProjectRecognizer_DisplayName();
        }
    }

    private void initializePipelineFactoryIfNull() {
        initializePipelineFactoryIfNull(null);
    }

    private void initializePipelineFactoryIfNull(String yamlJenkinsFile) {
        if (this.pipelineAsYamlWorkflowBranchProjectFactory == null) {
            this.yamlJenkinsFile = yamlJenkinsFile;
            ExtendedPipelineAsYamlWorkflowBranchProjectFactory
                .setInnerYamlJenkinsFile(this.yamlJenkinsFile);
            this.pipelineAsYamlWorkflowBranchProjectFactory = new ExtendedPipelineAsYamlWorkflowBranchProjectFactory(
                this.yamlJenkinsFile != null ? this.yamlJenkinsFile : YAML_JENKINS_FILE);
        }
    }

}
