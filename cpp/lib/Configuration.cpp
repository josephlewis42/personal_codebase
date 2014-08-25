/*
 * Configuration.cpp
 *
 * A simple configuration manager that looks up arbitrary key:value pairs.
 *
 * Copyright (c) 2013 Joseph Lewis <joehms22@gmail.com> | <joseph@josephlewis.net>
 * Licensed under the GPL 3
 */


#include "Configuration.h"
#include "Debug.h"

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>


#include <map>
#include <vector>
#include <string>
#include <string.h>
#include <utility>


// Static Class variable instantiation
std::mutex Configuration::_propertiesLock;

// Variables
std::string ROOT_ELEMENT = "configuration.";
std::string DEFAULT_XML_FILE_PATH = "config.xml";

const Logger LOG("Configuration: ");

Configuration::Configuration()
{
    _properties = new boost::property_tree::ptree();

    try
    {
        read_xml(DEFAULT_XML_FILE_PATH, *_properties, boost::property_tree::xml_parser::trim_whitespace);
    }
    catch(...)
    {
        std::cout << "Could not find configuration file: " << DEFAULT_XML_FILE_PATH << std::endl;
    }
}

Configuration::~Configuration()
{
}

std::string Configuration::gets(const std::string &key, const std::string &alt)
{
    std::lock_guard<std::mutex> lock(_propertiesLock);
    try
    {
        return _properties->get<std::string>(ROOT_ELEMENT + key);
    }
    catch(...)
    {
        _properties->put(ROOT_ELEMENT + key, alt);
        save();
        return alt;
    }
}


bool Configuration::getb(const std::string &key, bool alt)
{
    std::lock_guard<std::mutex> lock(_propertiesLock);

    try
    {
        return _properties->get<bool>(ROOT_ELEMENT + key);
    }
    catch(...)
    {
        _properties->put(ROOT_ELEMENT + key, alt);
        save();
        return alt;
    }
}


int Configuration::geti(const std::string &key, int alt)
{
    std::lock_guard<std::mutex> lock(_propertiesLock);

    try
    {
        return _properties->get<int>(ROOT_ELEMENT + key);
    }
    catch(...)
    {
        _properties->put(ROOT_ELEMENT + key, alt);
        save();
        return alt;
    }
}


double Configuration::getd(const std::string &key, double alt)
{
    std::lock_guard<std::mutex> lock(_propertiesLock);

    try
    {
        return _properties->get<double>(ROOT_ELEMENT + key);
    }
    catch(...)
    {
        _properties->put(ROOT_ELEMENT + key, alt);
        save();
        return alt;
    }
}


float Configuration::getf(const std::string &key, float alt)
{
    std::lock_guard<std::mutex> lock(_propertiesLock);

    try
    {
        return _properties->get<float>(ROOT_ELEMENT + key);
    }
    catch(...)
    {
        _properties->put(ROOT_ELEMENT + key, alt);
        save();
        return alt;
    }
}

void Configuration::set(const std::string &key, const std::string& value)
{
    std::lock_guard<std::mutex> lock(_propertiesLock);

    _properties->put(ROOT_ELEMENT + key, value);
    save();
}

void Configuration::setd(const std::string &key, const double value)
{
    set(key, std::to_string(value));
}

void Configuration::seti(const std::string &key, const int value)
{
    set(key, std::to_string(value));
}

void Configuration::save()
{
    try
    {
        boost::property_tree::xml_writer_settings<char> settings('\t', 1);
        write_xml(DEFAULT_XML_FILE_PATH, *_properties, std::locale(), settings);
    }
    catch(...)
    {
        LOG.warning() << "Can't save configuration";
    }
}



void Configuration::describe(const std::string &key,
              const std::string &domain,
              const std::string &usage,
              const std::string &unit,
              const std::string &note)
{
    std::lock_guard<std::mutex> lock(_descriptionsLock);

    std::string value = "";
    value += "* `" + key + "`\n";
    value += "\t* **Domain:** " + domain + "\n";
    value += "\t* **Usage:** " + usage + "\n";

    if(! unit.empty())
    {
        value += "\t* **Units:** " + unit + "\n";
    }

    if(! note.empty())
    {
        value += "\t* **Notes:** " + note + "\n";
    }

    _descriptions.insert(make_pair(key, value));
}

std::string Configuration::getDescription()
{
    std::lock_guard<std::mutex> lock(_descriptionsLock);

    std::string total = "";

    for (auto& kv : _descriptions)
    {
        total += kv.second;
    }

    return total;
}

