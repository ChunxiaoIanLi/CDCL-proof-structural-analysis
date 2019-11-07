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

/**
 * Exception to be thrown from {@link GraphInput} implementations. Exists
 * for the benefit of {@link GraphInput#get}'s exception specification.
 *
 * Useful in a {@link GraphInput} that doesn't want to catch
 * an exception that it itself encountered. 
 * 
 * @author tw team
 *
 */
public class InputException extends Exception {

	/**
	 * Generated ID for serialization. 
	 */
	private static final long serialVersionUID = 638210276339222780L;
	
	/**
	 * The exception that is being 
	 */
	public Exception originalException;
	
	/**
	 * Remembers an original <code>Exception</code>.
	 * @param e The original
	 */
	public InputException( Exception e ) {
		originalException = e;
	}
	
	public String toString() {
		return originalException.toString();
	}
	
}
