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
 
package nl.uu.cs.treewidth.timing;


/**
 *
 * Has better resolution than JavaSystemTime, but not sure if this is safe.
 * (That's why it is not the default.)
 * It definately isn't safe when multithreading on windows.
 * It also might not be when singlethreaded on a multiproc/core windows.
 * TODO Have a look at this sometime.
 *
 * @author tw team
 *
 */
public class JavaNanoTime implements TimeSource {

	/**
	 * @return in milliseconds.
	 */
	public long now() {
		return System.nanoTime() / 1000000;
	}

}