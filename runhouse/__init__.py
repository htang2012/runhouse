from runhouse.resources.asgi import Asgi, asgi
from runhouse.resources.blobs import blob, Blob, file, File
from runhouse.resources.envs import conda_env, CondaEnv, env, Env
from runhouse.resources.folders import Folder, folder, GCSFolder, S3Folder
from runhouse.resources.functionals.mapper import Mapper, mapper
from runhouse.resources.functions.aws_lambda import LambdaFunction
from runhouse.resources.functions.aws_lambda_factory import aws_lambda_fn
from runhouse.resources.functions.function import Function
from runhouse.resources.functions.function_factory import function
from runhouse.resources.hardware import (
    cluster,
    Cluster,
    kubernetes_cluster,
    ondemand_cluster,
    OnDemandCluster,
    sagemaker_cluster,
    SageMakerCluster,
)

# WARNING: Any built-in module that is imported here must be capitalized followed by all lowercase, or we will
# will not find the module class when attempting to reconstruct it from a config.
from runhouse.resources.kvstores.kvstore import Kvstore
from runhouse.resources.module import Module, module
from runhouse.resources.packages import git_package, GitPackage, package, Package
from runhouse.resources.provenance import capture_stdout, Run, run, RunStatus, RunType
from runhouse.resources.queues import Queue
from runhouse.resources.resource import Resource
from runhouse.resources.secrets import provider_secret, ProviderSecret, Secret, secret
from runhouse.resources.tables import Table, table
from runhouse.rns.secrets import Secrets  # Deprecated

from runhouse.rns.top_level_rns_fns import (
    current_folder,
    exists,
    get_local_cluster_object,
    ipython,
    load,
    locate,
    set_folder,
    unset_folder,
)

# Note these are global variables that are instantiated within globals.py:
from .globals import configs, obj_store

from .rns.login import login, logout

# Briefly keep for BC.
send = function

# Syntactic sugar
fn = function

_rh_here_stored = None


def __getattr__(name):
    global _rh_here_stored
    if name == "here":
        # If it's either the first time or the cluster was not initialized before, attempt to retrieve the cluster again
        if _rh_here_stored is None or _rh_here_stored == "file":
            _rh_here_stored = get_local_cluster_object()
        return _rh_here_stored

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__version__ = "0.0.16"
