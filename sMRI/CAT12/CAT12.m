% -------------------------------------------------------------------------
% This script is designed to execute a batch processing pipeline using SPM12 
% (Statistical Parametric Mapping) for medical image analysis. It is tailored
% for the CAT12 toolbox, typically used for voxel-based morphometry (VBM) and
% cortical thickness analysis. This script sets up the required job files and 
% executes them through SPM's job manager.
%
% Usage Instructions:
% (1) Update the `nrun` variable to specify the number of runs (datasets) to process.
% (2) Provide the path to your SPM12 installation and CAT12 job file.
% (3) Execute this script in MATLAB to process the data.
%
% Parameters:
% - `nrun`: The number of independent runs or datasets to process.
% - `jobfile`: A cell array containing the path to the CAT12 job file, which 
%    specifies the analysis pipeline.
% - `jobs`: A replicated array of the job file for all runs.
% - `inputs`: Placeholder for any additional inputs required by the job file.
%
% Example Usage:
% - Suppose you have one dataset to process using the CAT12 job file located at 
%   `/path/to/CAT12_job.m`. Update the `nrun` to `1` and set `jobfile` to 
%   `{'/path/to/CAT12_job.m'}`.
%
% - Run the script. Ensure SPM12 is in your MATLAB path.
%
% Notes:
% - Ensure that SPM12 and CAT12 are installed correctly and accessible.
% - Verify the paths for the job file and the SPM12 installation directory.
% - This script assumes that no additional input is required for the job file.
%
% Reference:
% - SPM12 Documentation: https://www.fil.ion.ucl.ac.uk/spm/
% - CAT12 Toolbox: http://www.neuro.uni-jena.de/cat/
% -------------------------------------------------------------------------

% Add SPM12 to the MATLAB path
% Adjust this path to the location of your SPM12 installation
addpath(genpath('/public/software/apps/MATLAB/matlab_compiler_2021b/toolbox/spm12/spm12'));

% Specify the number of runs (datasets) to process
nrun = 1; % Set this to the desired number of runs

% Define the path to the CAT12 job file
% This file should contain the specific analysis pipeline to execute
jobfile = {'/public/home/mazhw_i/cat/CAT12_job.m'};

% Replicate the job file for the specified number of runs
jobs = repmat(jobfile, 1, nrun);

% Initialize the inputs cell array
% This array holds any additional input arguments required for each run.
% Currently, no additional inputs are used.
inputs = cell(0, nrun);

% Loop through each run (if needed) to customize input parameters
for crun = 1:nrun
    % Placeholder for additional run-specific configuration
end

% Set SPM defaults for PET imaging
% This command initializes SPM with settings optimized for PET data.
spm('defaults', 'PET');

% Execute the batch job(s) using SPM's job manager
% `jobs` contains the batch files to run, and `inputs` passes any necessary inputs.
spm_jobman('run', jobs, inputs{:});

