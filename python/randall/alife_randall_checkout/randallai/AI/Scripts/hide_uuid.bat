REM       hide_uuid.bat -- Removes .* files in the parent's directory.
REM
REM       Copyright 2011 Joseph Lewis <joehms22@gmail.com>
REM
REM       This program is free software; you can redistribute it and/or modify
REM       it under the terms of the GNU General Public License as published by
REM       the Free Software Foundation; either version 2 of the License, or
REM       (at your option) any later version.
REM
REM       This program is distributed in the hope that it will be useful,
REM       but WITHOUT ANY WARRANTY; without even the implied warranty of
REM       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM       GNU General Public License for more details.
REM
REM       You should have received a copy of the GNU General Public License
REM       along with this program; if not, write to the Free Software
REM       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
REM       MA 02110-1301, USA.
cd %~dp0
cd ..
attrib +h .*
FOR /F "tokens=*" %%G IN ('DIR /B /AD /S') DO attrib +h "%%G\.*"
