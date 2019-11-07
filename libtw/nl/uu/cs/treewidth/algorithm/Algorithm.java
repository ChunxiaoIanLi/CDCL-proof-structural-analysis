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
import nl.uu.cs.treewidth.ngraph.NGraph;

/**
 * Base interface for all algorithms.
 * Using an Algorithm procedes in three steps.<br />
 * <ul><li>
 * Give it the graph to work on using <code>setInput</code>.
 * </li><li>
 * Have it do the actual computation using <code>run</code>.
 * </li><li> 
 * Retrieve the result. Methods to do this are provided in subinterfaces.
 * (See the list of `known subinterfaces.')
 * </li></ul>
 * 
 * @author tw team
 */
public interface Algorithm< D extends InputData> {

	/**
	 * Every algorithm has a name. This is for identification towards the user.
	 * @return Name of the algorithm.
	 */
	public abstract String getName();

	/**
	 * Sets the input the algorithm will run on.
	 * @param g The graph in standard graph format.
	 */
	public abstract void setInput(NGraph<D> g);

	/**
	 * Does the actual computation of the algorithm. The result is remembered but not returned. Get it using the appropriate return function (getUpperbound(), getLowerBound(), etc.).<br />
	 * Only works after setInput has been called.
	 */
	public abstract void run();
	
}