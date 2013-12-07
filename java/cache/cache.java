import java.util.HashMap;

/**
 * A cache mechanism, use it to store things you need to commonly look
 * up.
 * i.e.

Cache<String[]> dinos = new Cache<String[]>();

dinos.add(["Velociraptor", "Social", "Carnivore"], "Velociraptor");
dinos.add(["Compy", "Social", "Scavanger"], "Compy");

// Use multiple keys (they will be turned to Strings and concat'd)
dinos.add(["Dinosaurs", "Social", "Carnivore"], "Velociraptor", "Compy");
// Note that order matters!

 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 * Copyright 2011-11-29, Apache License
 *
 * @param <T> The type of the key to store.
 */
public class Cache<T> {
	
	private HashMap<String, T> m_map = new HashMap<String, T>();
	
	/**
	 * Empties the entire cache.
	 */
	public void clear()
	{
		m_map.clear();
	}
	
	/**
	 * Adds a value to the cache, with a key generated from the given objects.
	 * Order matters!
	 * 
	 * @param value
	 * @param keys
	 */
	public void add(T value, Object... keys)
	{
		m_map.put(getKey(keys), value);
	}
	
	/**
	 * Gets a key from the given objects.
	 * 
	 * @param keys
	 * @return
	 */
	private String getKey(Object[] keys)
	{
		String tmp = "";
		
		for(Object o : keys)
			tmp += o.toString();
		
		return tmp;
	}
	
	/**
	 * Gets an object from the database.
	 * 
	 * @param keys
	 * @return
	 */
	public T get(Object... keys)
	{
		return m_map.get(getKey(keys));
	}
	
	/**
	 * Checks if the map contains an object with
	 * the given keys.
	 * 
	 * @param keys
	 * @return
	 */
	public boolean contains(Object... keys)
	{
		return m_map.containsKey(getKey(keys));
	}
}

