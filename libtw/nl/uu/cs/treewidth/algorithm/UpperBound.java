/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth.algorithm;

import nl.uu.cs.treewidth.input.GraphInput.InputData;

/**
 * <p>Interface for algorithms that compute an upperbound.</p>
 * <p><code>getUpperBound()</code> must <i>always</i> return a valid upper
 * bound, even if <code>run()<code> has not been called yet. (Note that
 * <code>Integer.MAX_VALUE</code> (read: +infty) is considered to always
 * be an upperbound.)</p> 
 * 
 * @author tw team
 *
 */
public interface UpperBound< D extends InputData > extends Algorithm<D> {

	/**
	 * Returns the upperbound.
	 * 
	 * @return A valid upperbound. If run() has not been called, Integer.MAX_VALUE is returned.
	 */
	public abstract int getUpperBound();
	
}
