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
 * <p>Interface for algorithms that compute a lowerbound.</p>
 * <p><code>getLowerBound()</code> must <emph>always</emph> return
 * a valid lowerbound, even if run() has not been called yet.
 * (Note that -infty is always a valid lowerbound; use
 * <code>Integer.MIN_VALUE</code> to represent it.)</p> 
 * 
 * @author tw team
 *
 */
public interface LowerBound< D extends InputData > extends Algorithm<D> {

	/**
	 * @return A valid lowerbound. See class documentation for
	 * details.
	 */
	public abstract int getLowerBound();
	
	public static interface Creator {
		public LowerBound<InputData> create();
	}
	
}
