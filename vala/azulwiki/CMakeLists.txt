# Check http://webdev.elementaryos.org/docs/developer-guide/cmake for documentation

project (azulwiki)
cmake_minimum_required (VERSION 2.8)
cmake_policy (VERSION 2.6)

list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/vala)

#
# Base bits
#

enable_testing ()

set (DATADIR "${CMAKE_INSTALL_PREFIX}/share")
set (PKGDATADIR "${DATADIR}/azulwiki")
set (GETTEXT_PACKAGE "azulwiki")
set (RELEASE_NAME "First")
set (VERSION "0.1")
set (VERSION_INFO "Release")
set (CMAKE_C_FLAGS "-ggdb")
set (PREFIX ${CMAKE_INSTALL_PREFIX})
set (DOLLAR "$")

list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

#configure_file (${CMAKE_SOURCE_DIR}/src/Config.vala.cmake ${CMAKE_BINARY_DIR}/src/Config.vala)
#add_definitions(-DGETTEXT_PACKAGE=\"${GETTEXT_PACKAGE}\")

find_package(PkgConfig)
pkg_check_modules(DEPS REQUIRED gtk+-3.0 sqlite3 granite glib-2.0 webkitgtk-3.0 gee-1.0 gdk-3.0)

add_definitions(${DEPS_CFLAGS})

link_libraries(${DEPS_LIBRARIES})
link_directories(${DEPS_LIBRARY_DIRS})

find_package(Vala REQUIRED)
include(ValaVersion)
ensure_vala_version("0.14.0" MINIMUM)

include(ValaPrecompile)
vala_precompile(VALA_C
	src/azul.vala
    src/data_connection.vala
    src/settings.vala
PACKAGES
    gtk+-3.0
    sqlite3
    glib-2.0
    webkitgtk-3.0
    gee-1.0
    granite
    gdk-3.0
    
OPTIONS
    --thread
    --vapidir=${CMAKE_CURRENT_SOURCE_DIR}/vapi/
    )

#add_subdirectory (po)

add_executable (azulwiki ${VALA_C})

install(TARGETS azulwiki RUNTIME DESTINATION bin)

install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/azulwiki.desktop DESTINATION share/applications)

install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/azulwiki.svg DESTINATION share/icons/hicolor/48x48/apps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/gnome-mime-application-x-azulwikidocument.svg DESTINATION share/pixmaps)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/data/azulwiki.xml DESTINATION share/mime/packages)


execute_process(COMMAND update-mime-database "${CMAKE_INSTALL_PREFIX}/share/mime")
execute_process(COMMAND update-desktop-database)
