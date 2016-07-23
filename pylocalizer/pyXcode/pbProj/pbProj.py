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

from pbPlist import pbPlist

from .PBX_Constants import *
from .PBX_Lookup import *

class PBXProj(object):
    
    def __init__(self, file_path):
        plist = pbPlist.PBPlist(file_path)
        
        contents = plist.root.nativeType()
        
        self.pbxObjects = set()
        self.pbxIdentifier = None
        self.pbxRootObject = None
        self.pbxObjectVersion = 0
        self.pbxArchiveVersion = 0
        if contents != None:
            # get the path that we read from
            self.pbxFilePath = plist.file_path
            
            # get the root object identifier
            self.pbxIdentifier = contents.get(kPBX_rootObject, None)
            
            # get the archive version number
            archive_version = contents.get(kPBX_archiveVersion, None)
            if archive_version:
                self.pbxArchiveVersion = int(archive_version)
            
            # get the object version number
            object_version = contents.get(kPBX_objectVersion, None)
            if object_version:
                self.pbxObjectVersion = int(object_version)
            
            # get the classes
            self.pbxClasses = contents.get(kPBX_classes, None)
            
            # get all the objects
            objects_dict = contents.get(kPBX_objects, None)
            
            for entry in objects_dict.keys():
                entry_dict = objects_dict.get(entry, None)
                if entry_dict:
                    object_item = PBX_Type_Resolver(entry, entry_dict)
                    self.pbxObjects.add(object_item)
            
            self.pbxRootObject = self.objectForIdentifier(self.pbxIdentifier) 
            self.pbxRootObject.resolveGraph(self)
            
    def __repr__(self):
        if self.isValid():
            return '<%s : %s : %s>' % (self.__class__.__name__, self.pbxIdentifier,  self.pbxFilePath)
        else:
            return '<%s : INVALID OBJECT>' % (self.__class__.__name__)
    
    def __attrs(self):
        return (self.pbxIdentifier, self.pbxFilePath)

    def __eq__(self, other):
        return isinstance(other, PBXProj) and self.pbxIdentifier == other.pbxIdentifier and self.pbxFilePath == other.pbxFilePath

    def __hash__(self):
        return hash(self.__attrs())
    
    def isValid(self):
        return self.pbxIdentifier != None
        
    def objectForIdentifier(self, identifier):
        """
        Returns the parsed object from the project file for matching identifier, if no matching object is found it will return None.
        """
        result = None
        if self.isValid():
            filter_results = filter(lambda obj: obj.identifier == identifier, self.pbxObjects)
            if len(filter_results) > 0:
                result = filter_results[0]
        return result
    
    def projects(self):
        """
        This method returns a set of 'xcodeproj' objects that represents any referenced 
        xcodeproj files in this project.
        """
        subprojects = set();
        if self.isValid():
            for path in self.__subproject_paths():
                subprojects.add(path)
        return subprojects;
        
    
    def __subproject_paths(self):
        """
        This method is for returning a list of paths to referenced project files in this
        xcodeproj file.
        """
        paths = list()
        if self.isValid():
            project_references = self.pbxRootObject.get(kPBX_PROJECT_projectReferences, None)
            if project_references:
                for project_dict in project_references:
                    project_ref = project_dict[kPBX_PROJECTREF_ProjectRef]
                    paths.append(project_ref)
        return paths;
    
    def targets(self):
        """
        This method will return a list of build targets that are associated with this xcodeproj.
        """
        targets = list()
        if self.isValid():
            target_list = self.pbxRootObject.get(kPBX_PROJECT_targets, None)
            if target_list:
                targets.extend(target_list)
        return targets