# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pylocalizer
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys

from pyxcwsdata.xcworkspacedata import xcworkspacedata

from Helpers import Logger

from xcodeproj import xcodeproj

class xcworkspace(object):
    
    def __init__(self, xcworkspace_file_path):
        if os.path.exists(xcworkspace_file_path):
            if xcworkspace_file_path.endswith('.xcworkspace'):
                self.filePath = xcworkspace_file_path
                
                # loading the pbxproj
                workspace_data_path = os.path.join(self.filePath, 'contents.xcworkspacedata')
                if os.path.exists(workspace_data_path):
                    self.contentsFile = xcworkspacedata(workspace_data_path)
                else:
                    Logger.write().error('Could not find the xcworkspacedata file!')
                
                # load schemes
                self.schemes = xcscheme.LoadSchemes(self.filePath)
                
            else:
                Logger.write().error('Not a Xcode workspace file!')
        else:
            Logger.write().error('Could not find the Xcode workspace file!')
    
    def projects(self):
        project_list = list()
        for project_file_path in self.contentsFile.projects():
            project_list.append(xcodeproj(project_file_path))
        return project_list

#    def hasSchemeWithName(self, scheme_name):
#        """
#        This method is used for both 'xcworkspace' and 'xcodeproj' classes. It returns a two
#        element tuple that contains the following:
#        
#        First element:
#            A 'True' or 'False' value indicating if a scheme with the passed name was found in 
#            this project or workspace file.
#        
#        Second element:
#            The scheme object if a scheme with matching name was found, None otherwise.
#        """
#        found_scheme = None
#        scheme_filter = filter(lambda scheme: scheme.name == scheme_name, self.schemes)
#        if len(scheme_filter) > 0:
#            found_scheme = scheme_filter[0]
#        return (found_scheme != None, found_scheme)