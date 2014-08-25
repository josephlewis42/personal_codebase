/**
 * Copyright 2014 Joseph Lewis <joseph@josephlewis.net>
 *
 * This file is part of University of Denver Autopilot.
 * Dual licensed under the GPL v 3 and the Apache 2.0 License
 *
**/

#ifndef PATH_H_
#define PATH_H_

#include <string>

/** This class handles filesystem paths.
**/
class Path
{
    private:
    std::string _path;

    int remove_all(const char* path);

    public:

    /// Constructs a path in the current working directory
    Path();

    /// Constructs a path with the given initial file
    Path(std::string initial)
        :_path(initial)
        {};

    Path(const char* initial)
        :_path(initial)
        {};

    bool has_extension();

    /// Check if the path exists
    bool exists();

    /// Reinitialize path
    bool clear();

    /// Recursively removes a directory.
    int remove_all();

    /// Returns the extension of the path or a blank string if none exists
    std::string get_extension();

    /** Recursively makes a directory.
      * src: http://nion.modprobe.de/blog/archives/357-Recursive-directory-creation.html
     **/
    void create_directories();

    std::string toString() const;

    const char* c_str() const;

    friend Path operator/(const Path &p, const char* toappend);
    friend Path operator/(const Path &p, const std::string toappend);
    Path& operator/=(const char* right);
    Path& operator/=(const std::string right);
};


#endif // PATH_H_

