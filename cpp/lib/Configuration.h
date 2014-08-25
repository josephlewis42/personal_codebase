/*
 * Configuration.h
 *
 * A simple configuration manager that looks up arbitrary key:value pairs.
 *
 * Copyright (c) 2013 Joseph Lewis <joehms22@gmail.com> | <joseph@josephlewis.net>
 * Licensed under the GPL 3
 *
 */

#ifndef CONFIGURATION_H_
#define CONFIGURATION_H_

#include <string>
#include <mutex>
#include <boost/property_tree/ptree_fwd.hpp>
#include <vector>
#include <map>
#include "Singleton.h"


class Configuration : public Singleton<Configuration>
{
    friend class Singleton<Configuration>;

public:

    // Loads the values from the given properties file.
    void loadProperties(std::string path);

    // Returns a string from the configuration.
    std::string gets(const std::string &key, const std::string &alt="");

    // Returns a bool from the configuration
    bool getb(const std::string &key, bool alt=false);

    // Returns an int from the configuration.
    int geti(const std::string &key, int alt=0);

    // Returns a float from the configuration
    float getf(const std::string &key, float alt=0.0f);

    // Returns a double from the configuration
    double getd(const std::string &key, double alt=0.0);

    /**
     * Sets a path to be a value.
     */
    void set(const std::string &key, const std::string& value);

    /**
     * Sets a path to be a double value
     *
     * @param key - the key to store the value under
     * @param value - the value of the param
     */
    void setd(const std::string &key, const double value);

    /**
     * Sets a path to be an int value
     *
     * @param key - the key to store the value under
     * @param value - the value of the param
     */
    void seti(const std::string &key, const int value);

    /**
     * Sets a description for the given key. Note that basic markdown can be used
     * when setting these descriptions.
     *
     * @param key - the key to set the description for
     * @param domain - the domain of the key (e.g. 1-100 or non-negative integers)
     * @param usage - how the key is used internally
     * @param units - the units of this value (optional)
     * @param note - a note about the key (optional)
     **/
    void describe(const std::string &key,
                  const std::string &domain,
                  const std::string &usage,
                  const std::string &units="",
                  const std::string &note="");


    /**
     * Returns the description for the whole configuration file.
     **/
    std::string getDescription();

private:
    boost::property_tree::ptree* _properties;
    static std::mutex _propertiesLock;
    std::map<std::string, std::string> _descriptions;
    std::mutex _descriptionsLock;


    Configuration();
    virtual ~Configuration();

    void save();

};


/**
 * Allows you to perform configuration operations on a sub-tree of the main
 * configuration as if it were an independent configuration tree.
 *
 */
class ConfigurationSubTree
{

private:
    std::string _prefix;

public:
    ConfigurationSubTree(std::string prefix)
        :_prefix(prefix + ".") {}
    virtual ~ConfigurationSubTree() {};

    /// Returns a string from the configuration.
    std::string configGets(const std::string &key, const std::string &alt="")
    {
        return Configuration::getInstance()->gets(_prefix + key, alt);
    }

    /// Returns a bool from the configuration
    bool configGetb(const std::string &key, bool alt=false)
    {
        return Configuration::getInstance()->getb(_prefix + key, alt);
    }

    /// Returns an int from the configuration.
    int configGeti(const std::string &key, int alt=0)
    {
        return Configuration::getInstance()->geti(_prefix + key, alt);
    }

    /// Returns a float from the configuration
    float configGetf(const std::string &key, float alt=0.0f)
    {
        return Configuration::getInstance()->getf(_prefix + key, alt);
    }

    /// Returns a double from the configuration
    double configGetd(const std::string &key, double alt=0.0)
    {
        return Configuration::getInstance()->getd(_prefix + key, alt);
    }

    /**
     * Sets a path to be a value.
     */
    void configSet(const std::string &key, const std::string& value)
    {
        Configuration::getInstance()->set(_prefix + key, value);
    }

    /**
     * Sets a path to be a double value
     *
     * @param key - the key to store the value under
     * @param value - the value of the param
     */
    void configSetd(const std::string &key, const double value)
    {
        return Configuration::getInstance()->setd(_prefix + key, value);
    }

    /**
     * Sets a path to be an int value
     *
     * @param key - the key to store the value under
     * @param value - the value of the param
     */
    void configSeti(const std::string &key, const int value)
    {
        Configuration::getInstance()->seti(_prefix + key, value);
    }

    /**
     * Sets a description for the given key. Note that basic HTML can be used
     * when setting these descriptions.
     *
     * @param key - the key to set the description for
     * @param domain - the domain of the key (e.g. 1-100 or non-negative integers)
     * @param usage - how the key is used internally
     * @param units - the units of this value (optional)
     * @param note - a note about the key (optional)
     **/
    void configDescribe(const std::string &key,
                  const std::string &domain,
                  const std::string &usage,
                  const std::string &units="",
                  const std::string &note="")
    {
        Configuration::getInstance()->describe(_prefix + key, domain, usage, units, note);
    }
};

#endif /* CONFIGURATION_H_ */

