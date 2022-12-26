#!/usr/bin/env sh

# This script sets environment variables and aliases to
# allow the usage of a custom tiscamera installation


if [ -z "${PKG_CONFIG_PATH}" ]; then
    export PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig:${PKG_CONFIG_PATH}"
else
    export PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig"
fi

if [ -z "${GST_PLUGIN_PATH_1_0}" ]; then
    export GST_PLUGIN_PATH_1_0="/usr/lib/x86_64-linux-gnu/gstreamer-1.0:${GST_PLUGIN_PATH_1_0}"
else
    export GST_PLUGIN_PATH_1_0="/usr/lib/x86_64-linux-gnu/gstreamer-1.0"
fi

if [ -z "${LD_RUN_PATH}" ]; then
    export LD_RUN_PATH="/usr/lib:${LD_LIBRARY_PATH}"
else
    export LD_RUN_PATH="/usr/lib"
fi

if [ -z "${GI_TYPELIB_PATH}" ]; then
    export GI_TYPELIB_PATH="/usr/lib/x86_64-linux-gnu/girepository-1.0:${GI_TYPELIB_PATH}"
else
    export GI_TYPELIB_PATH="/usr/lib/x86_64-linux-gnu/girepository-1.0:"
fi

if [ -z "${LD_LIBRARY_PATH}" ]; then
    export LD_LIBRARY_PATH="/usr/lib:/usr/lib/tcam-0:${LD_RUN_PATH}"
else
    export LD_LIBRARY_PATH="/usr/lib:/usr/lib/tcam-0"
fi

if [ -z "${LIBRARY_PATH}" ]; then
    export LIBRARY_PATH="/usr/lib:/usr/lib/tcam-0:${LD_RUN_PATH}"
else
    export LIBRARY_PATH="/usr/lib:/usr/lib/tcam-0"
fi

if [ -z "${PYTHONPATH}" ]; then
    export PYTHONPATH=":${PYTHONPATH}"
else
    export PYTHONPATH=""
fi


export PATH="/usr/bin:${PATH}"
