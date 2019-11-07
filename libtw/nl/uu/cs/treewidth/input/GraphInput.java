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
 
package nl.uu.cs.treewidth.input;

import nl.uu.cs.treewidth.ngraph.NGraph;

/**
 * <p>Interface for classes that can return a Graph.</p> 
 * <p>Using this interface the program can be oblivious of where the
 * graph data is coming from (e.g. read a DGF file, or generate some
 * random graph.</p>
 * <p>
 * <i>Example usage:</i>
 * </p>
 * <pre>
 * GraphInput input = new DgfReader( "myGraph.dgf" );
 * NGraph g = null;
 * try {
 *     g = input.get();
 * } catch (InputException e) { ... }
 * </pre>
 * 
 * <p>
 * <i>Example usage:</i>
 * </p>
 * <pre>
 * GraphInput input = new GridGraphGenerator( 3, 7 );
 * NGraph g = null;
 * try {
 *     g = input.get();
 * } catch (InputException e) { ... }
 * </pre>
 * 
 * @author tw team
 *
 */
public interface GraphInput {
	
	public static class InputData {
		public InputData() {}
		public InputData( int id, String name ) {
			this.id = id;
			this.name = name;
		}
		public int id;
		public String name;
		public String toString() {
			return name;
		}
	}

	/**
	 * Return a graph. Implementing classes will have additional
	 * interface to give meaning to this call.
	 * 
	 * @return A graph; entirely up to implementing classes what
	 * to return.
	 * @throws InputException
	 */
	abstract public NGraph<InputData> get() throws InputException;
	
}
