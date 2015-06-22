# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
 
# Copyright (c) 2012-2015 Christian Schwarz
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# General imports
import copy
from numbers import Number
from math import sqrt

# imports from pycast
from pycastobject import PyCastObject
from decorators import optimized
from timeseries import MultiDimensionalTimeSeries

def sign(a, b):
    """Return a with the algebraic sign of b"""
    return (b/abs(b)) * a

def pythag(a, b):
    """Computer c = (a^2 + b^2)^0.5 without destructive underflow or overflow

    It solves the Pythagorean theorem a^2 + b^2 = c^2
    """
    absA = abs(a)
    absB = abs(b)
    if absA > absB:
        return absA * sqrt(1.0 + (absB / float(absA)) ** 2)
    elif absB == 0.0:
        return 0.0
    else:
        return absB * sqrt(1.0 + (absA / float(absB)) ** 2)

class Matrix(PyCastObject):
    """A Matrix instance stores all relevant data of a matrix.

    It provides a number of Matrix operations, such as multiplication,
    transformation and inversion.
    """
    # default number of digits after decimal point which are printed
    defaultStringPrecision = 3

    def __init__(self, columns, rows, oneDimArray=None, rowBased=True, isOneDimArray=True):
        """Initialize the Matrix with the given number of columns and rows.

        :param integer columns:     The number of columns for the Matrix.
        :param integer rows:        The number of rows for the Matrix.
        :param list oneDimArray:    The values for the Matrix in a based
                                    one dimensional list. Depending on the
                                    rowBased parameter, the first n values
                                    (n = the number of rows) represents either
                                    the first row or the first column.
                                    The length of oneDimArray has to be
                                    columns * rows.
                                    If isOneDimArray is False this should be a
                                    two dimensonal list.
        :param boolean rowBased:    Only necessary if the oneDimArray is given.
                                    Indicates whether the oneDimArray combines
                                    rows together (rowBased=True) or columns
                                    (rowBased=False)
        :param boolean isOneDimArray: Indicates whether the parameter
                                    oneDimArray is a one dimensional array or
                                    a two dimensional array.

        :raise: Raises an :py:exc:`ValueError` if:
            - columns < 1 or
            - rows < 1
            - len(oneDimArray) != columns * rows
        """
        if columns < 1 or rows < 1:
            raise ValueError("At least one row and one column is necessary")
        super(Matrix, self).__init__()
        self._columns = columns
        self._rows = rows
        if oneDimArray is None:
            self.matrix = [[0.0 for i in xrange(rows)] for j in xrange(columns)]
        elif isOneDimArray:
            if len(oneDimArray) != columns * rows:
                raise ValueError("""Size of array does not fit in Matrix
                    with %d rows and %d columns""" % (rows, columns))
            if rowBased:
                self.matrix = []
                for j in xrange(columns):
                    self.matrix.append([])
                    for i in xrange(rows):
                        self.matrix[j].append(oneDimArray[i * columns + j])
            else:
                self.matrix = [[oneDimArray[j * rows + i] for i in xrange(rows)] for j in xrange(columns)]
        else:
            self._initialize_with_array(oneDimArray, rowBased)

        self._stringPrecision = Matrix.defaultStringPrecision

    def __str__(self):
        """Return a String representation of the :py:obj:`self`

        The number of digits after the decimal point can be specified using
            :py:meth:`self.set_str_precision` """
        rep = "%d x %d Matrix\n" % (self.get_height(), self.get_width())
        # get value with the most digits before the decimal point.
        max_val = max(max(abs(min(row)), max(row)) for row in self.matrix)
        # set width for each entry.
        # places before decimal place, places after decimal place +
        # decimal point, sign and one empty space.
        width = len(str(int(max_val))) + self._stringPrecision + 3
        for row in xrange(self.get_height()):
            for col in xrange(self.get_width()):
                val = float(self.get_value(col, row))
                rep += "{num: {width}.{prec}f}".format(num=val, width=width, prec=self._stringPrecision)
            rep += "\n"
        return rep

    def __eq__(self, otherMatrix):
        """Return if :py:obj:`self` and the other Matrix are equal

        Matrices are equal to each other if:
            - the values are equal at all positions.

        :return:    :py:const:`True` if Matrix objects are equal,
                    :py:const:`False` mulotherwise.
        :rtype: boolean
        """
        if self.matrix != otherMatrix.matrix:
            return False

        return True

    def __ne__(self, otherMatrix):
        """Return if :py:obj:`self` and the other Matrix are not equal"""
        return not self == otherMatrix

    def _initialize_with_array(self, data, rowBased=True):
        """Set the matrix values from a two dimensional list."""
        if rowBased:
            self.matrix = []
            if len(data) != self._rows:
                raise ValueError("Size of Matrix does not match")
            for col in xrange(self._columns):
                self.matrix.append([])
                for row in xrange(self._rows):
                    if len(data[row]) != self._columns:
                        raise ValueError("Size of Matrix does not match")
                    self.matrix[col].append(data[row][col])
        else:
            if len(data) != self._columns:
                raise ValueError("Size of Matrix does not match")
            for col in data:
                if len(col) != self._rows:
                    raise ValueError("Size of Matrix does not match")
            self.matrix = copy.deepcopy(data)

    @classmethod
    def from_timeseries(cls, timeSeries):
        """Create a new Matrix instance from a TimeSeries or MultiDimensionalTimeSeries

        :param TimeSeries timeSeries: The TimeSeries, which should be used to
                create a new Matrix.
        :return:    A Matrix with the values of the timeSeries. Each row of
                    the Matrix represents one entry of the timeSeries.
                    The time of an entry is ignored in the matrix.
        :rtype:     Matrix

        :raise:     Raises an :py:exc:`ValueError`, if the timeSeries is empty.
        """
        width = 1

        if isinstance(timeSeries, MultiDimensionalTimeSeries):
            width = timeSeries.dimension_count()
            
        matrixData = [[] for dummy in xrange(width)]

        for entry in timeSeries:
            for col in xrange(1, len(entry)):
                matrixData[col - 1].append(entry[col])
        if not matrixData[0]:
            raise ValueError("Cannot create Matrix from empty Timeseries")
        mtrx = Matrix.from_two_dim_array(len(matrixData), len(matrixData[0]), matrixData)

        # mtrx.initialize(matrixData, rowBased=False)
        return mtrx

    @classmethod
    def from_two_dim_array(cls, cols, rows, twoDimArray):
        """Create a new Matrix instance from a two dimensional array.

        :param integer columns:     The number of columns for the Matrix.
        :param integer rows:        The number of rows for the Matrix.
        :param list twoDimArray:    A two dimensional column based array
                                    with the values of the matrix.
        :raise: Raises an :py:exc:`ValueError` if:
            - columns < 1 or
            - rows < 1
            - the size of the parameter does not match with the size of
              the Matrix.
        """
        return Matrix(cols, rows, twoDimArray, rowBased=False, isOneDimArray=False)

    def initialize(self, datalist, rowBased=True):
        """Initialize :py:obj:`self` with the values stored in the two dimensional list.

        :param list datalist: A list representing the matrix rows
                    containing lists representing the columns for each row.
                    The values in the List must be numeric
        :param boolean rowBased: Indicates wether the datalist is row or
            column based. Has to be True if datalist[i] is the i'th row,
            or False if datalist[i] is the i'th column

        :raise: Raises an :py:exc:`ValueError` if the size of the parameter
            does not match with the size of the Matrix.
        :note: The values in the list are not checked for the correct type.
        """
        self._initialize_with_array(datalist, rowBased)

    def to_multi_dim_timeseries(self):
        """Return a TimeSeries with the values of :py:obj:`self`

        The index of the row is used for the timestamp

        :return:    Return a new MultiDimensionalTimeSeries with the values
                    of the Matrix
        :rtype:     MultiDimensionalTimeSeries
        """
        ts = MultiDimensionalTimeSeries(dimensions=self.get_width())
        for row in xrange(self.get_height()):
            newEntry = []
            for col in xrange(self.get_width()):
                newEntry.append(self.get_value(col, row))
            ts.add_entry(row, newEntry)
        return ts

    def get_array(self, rowBased=True):
        """Return a two dimensional list with the values of the :py:obj:`self`.

        :param boolean rowBased: Indicates wether the returned list should be
            row or column based. Has to be True if list[i] should be the i'th
            row, False if list[i] should be the i'th column.

        :return:    Returns a list representing the matrix rows
                    containing lists representing the columns for each row.
        :rtype: list
        """
        if rowBased:
            array = []
            for row in xrange(self._rows):
                newRow = []
                for col in xrange(self._columns):
                    newRow.append(self.get_value(col, row))
                array.append(newRow)
            return array
        return copy.deepcopy(self.matrix)

    def get_matrix_from_list(self, rows, columns, matrix_list, rowBased=True):
        """Create a new Matrix instance from a matrix_list.

        :note: This method is used to create a Matrix instance using cpython.
        :param integer rows:        The height of the Matrix.
        :param integer columns:     The width of the Matrix.
        :param matrix_list:         A one dimensional list containing the
                                    values for Matrix. Depending on the
                                    rowBased parameter, either the rows are
                                    combined or the columns.
        :param rowBased Boolean:    Only necessary if the oneDimArray is given.
                                    Indicates whether the oneDimArray combines
                                    rows together (rowBased=True) or columns
                                    (rowBased=False).
        """
        resultMatrix = Matrix(columns, rows, matrix_list, rowBased)
        return resultMatrix

    def set_value(self, column, row, value):
        """Set the value of the Matrix at the specified column and row.

        :param integer column:  The index for the column (starting at 0)
        :param integer row:     The index for the row (starting at 0)
        :param numeric value:   The new value at the given column/row

        :raise:     Raises an :py:exc:`IndexError` if the index is out of xrange.
        """
        self.matrix[column][row] = value

    def get_value(self, column, row):
        """Return the value of :py:obj:`self` at the specified column and row.

        :param integer column:  The index for the column (starting at 0)
        :param integer row:     The index for the row (starting at 0)

        :raise:     Raises an :py:exc:`IndexError` if the index is out of xrange.
        """
        return self.matrix[column][row]

    def get_height(self):
        "Return the number of rows of the Matrix"
        return self._rows

    def get_width(self):
        """Return the number of columns of the Matrix"""
        return self._columns

    def set_string_precision(self, precision):
        """Set the number of digits after the decimal point used to print the Matrix

        :param integer precision: The number of digits to which the values
            should be rounded when the Matrix is printed.

        :raise: Raises an :py:exc:`ValueError` if precision is negative.
        """
        if precision < 0:
            raise ValueError("precision cannot be negative")
        self._stringPrecision = precision

    def invers(self):
        """Return the invers matrix, if it can be calculated

        :return:    Returns a new Matrix containing the invers
        :rtype:     Matrix

        :raise:     Raises an :py:exc:`ValueError` if the matrix is not inversible

        :note:      Only a squared matrix with a determinant != 0 can be inverted.
        :todo:      Reduce amount of create and copy operations
        """

        if self._columns != self._rows:
            raise ValueError("A square matrix is needed")
        mArray = self.get_array(False)
        appList = [0] * self._columns

        # add identity matrix to array in order to use gauss jordan algorithm
        for col in xrange(self._columns):
            mArray.append(appList[:])
            mArray[self._columns + col][col] = 1
        # create new Matrix and execute gass jordan algorithm
        exMatrix = Matrix.from_two_dim_array(2 * self._columns, self._rows, mArray)
        gjResult = exMatrix.gauss_jordan()
        # remove identity matrix from left side
        # TODO Implement slicing directly for Matrix
        gjResult.matrix = gjResult.matrix[self._columns:]
        gjResult._columns = len(gjResult.matrix)
        return gjResult

    def __copy__(self):
        """Return a new clone of the Matrix

        :return:    Returns a Matrix containing the same data and
                    configuration as self.
                    It does not copy super classes, but the
                    optimization status (True/False) is copied
        :rtype:     Matrix
        """
        mtrx = Matrix.from_two_dim_array(self._columns, self._rows, self.matrix)
        ## copy of immmutable Boolean.
        mtrx.optimizationEnabled = self.optimizationEnabled

        return mtrx

    def __mul__(self, other):
        """Return the result of the matrixmultiplication or a multiple of the matrix

        :param Matrix or Number other: The matrix, which should be multiplied.

        :return:    Returns a new Matrix with the result of the multiplication
        :rtype:     Matrix

        :raise: Raises an :py:exc:`ValueError` if
                -   the number of columns of the Matrix does not match witch
                -   the number of rows of the given matrix.
        :raise: Raises an :py:exc:`TypeError` if the input parameter is not
                    a Matrix or a number

        """
        if isinstance(other, Matrix):
            return self.matrix_multiplication(other)
        elif isinstance(other, Number):
            return self.multiply(other)
        else:
            raise TypeError("Can't multiply Matrix with type %s" % type(other).__name__)

    def __rmul__(self, other):
        """Return multiple of Matrix

        :return: Returns a
        :raise: Raises an :py:exc:`ValueError` if the input parameter is not a number
        """
        if isinstance(other, Number):
            return self.multiply(other)
        else:
            raise TypeError("Can't multiply Matrix with type %s" % type(other).__name__)

    def is_matrix_mult_possible(self, matrix):
        """Return True if :py:obj:`self` can be multiplied with the other matrix, False otherwise"""
        if self._columns != matrix.get_height():
            return False
        return True

    @optimized
    def matrix_multiplication(self, matrix):
        """Multiply :py:obj:`self` with the given matrix and return result matrix.

        param Matrix matrix: The matrix, which should be multiplied.

        :return:    Returns a new Matrix with the result of the multiplication
        :rtype:     Matrix

        :note: Make sure, that the matrices can be multiplied.
                The number of columns of the Matrix instance must match with
                the number of rows of the Matrix given as parameter.
                Use is_matrix_mult_possible(matrix) to test.
        """
        resultMatrix = Matrix(matrix.get_width(), self.get_height())
        for r_row in xrange(self._rows):
            for r_col in xrange(matrix.get_width()):
                #blockwise matrix multiplication hack
                if isinstance(self.get_array()[0][0], Matrix):
                    blocksize = self.get_array()[0][0].get_width()
                    valueT = Matrix(blocksize, blocksize)
                else:
                    valueT = 0
                for column in xrange(matrix.get_height()):
                    valueT += self.get_value(column, r_row) * matrix.get_value(r_col, column)
                resultMatrix.set_value(r_col, r_row, valueT)
        return resultMatrix

    def matrix_multiplication_blockwise(self, matrix, blocksize):
        """
        http://en.wikipedia.org/wiki/Block_matrix#Block_matrix_multiplication
        """
        #Create the blockwise version of self and matrix
        selfBlockwise = self.matrix_to_blockmatrix(blocksize)
        matrixBlockwise = matrix.matrix_to_blockmatrix(blocksize)

        return (selfBlockwise * matrixBlockwise).flatten()

    def flatten(self):
        """
        If the current Matrix consists of Blockmatrixes as elementes method
        flattens the Matrix into one Matrix only consisting of the 2nd level
        elements

        [[[1 2] [[3 4]   to [[1 2 3 4]
          [5 6]] [7 8]]]     [5 6 7 8]]
        """
        blocksize = self.get_array()[0][0].get_width()
        width = self.get_width() * blocksize
        
        columnsNew = [[] for dummy in xrange(width)]

        for row in self.get_array():
            index = 0
            for submatrix in row:
                for column in submatrix.get_array(False):
                    columnsNew[index] += column
                    index += 1

        columnsFlat = sum(columnsNew, [])
        return Matrix(width, len(columnsNew[0]), columnsFlat, rowBased=False)

    def matrix_to_blockmatrix(self, blocksize):
        """
        turns an n*m Matrix into a (n/blocksize)*(m/blocksize matrix).
        Each element is another blocksize*blocksize matrix.
        """
        if self.get_width() % blocksize or self.get_height() % blocksize:
            raise ValueError("Number of rows and columns have to be evenly dividable by blocksize")
        selfBlocks = []
        for columnIndex in range(0, self.get_width() - 1, blocksize):
            for rowIndex in range(0, self.get_height() - 1, blocksize):
                currentBlock = []
                for blockRows in self.get_array(False)[columnIndex:columnIndex + blocksize]:
                    currentBlock += blockRows[rowIndex:rowIndex + blocksize]
                selfBlocks.append(Matrix(blocksize, blocksize, currentBlock, rowBased=False))
        return Matrix(self.get_width() / blocksize, self.get_height() / blocksize, selfBlocks, rowBased=False)

#    def matrix_multiplication_scipy(self, matrix):
#        a = np.matrix(self.get_array())
#        b = np.matrix(matrix.get_array())
#        c = (a*b)
#       c_list = c.tolist()
#      result = Matrix(len(c_list[0]), len(c_list), None)
#        result.initialize(c_list)
#        return result

    def multiply(self, multiplicator):
        """Return a new Matrix with a multiple.

        :param Number multiplicator:  The number to calculate the multiple

        :return:    The Matrix with the the multiple.
        :rtype:     Matrix
        """
        result = Matrix(self.get_width(), self.get_height())
        for row in xrange(self.get_height()):
            for col in xrange(self.get_width()):
                result.set_value(col, row, self.get_value(col, row) * multiplicator)
        return result

    def transform(self):
        """Return a new transformed matrix.

        :return:    Returns a new transformed Matrix
        :rtype:     Matrix
        """
        t_matrix = Matrix(self._rows, self._columns)
        for col_i, col in enumerate(self.matrix):
            for row_i, entry in enumerate(col):
                t_matrix.set_value(row_i, col_i, entry)
        return t_matrix

    def gauss_jordan(self):
        """Reduce :py:obj:`self` to row echelon form.

        :return:    Returns :py:obj:`self` in row echelon form for convenience.
        :rtype:     Matrix
        :raise:     Raises an :py:exc:`ValueError` if:
                        - the matrix rows < columns
                        - the matrix is not invertible
                    In this case :py:obj:`self` is not changed.
        """

        mArray = self.get_array(rowBased=False)
        width = self.get_width()
        height = self.get_height()
        if not height < width:
            raise ValueError("""Not enough rows""")
        # Start with complete matrix and remove in each iteration
        # the first row and the first column
        for offset in xrange(height):
            ## Switch lines, if current first value is 0
            if mArray[offset][offset] == 0:
                for i in xrange(offset + 1, height):
                    if mArray[offset][i] != 0:
                        tmp = []
                        for j in xrange(offset, width):
                            tmp.append(mArray[j][offset])
                        # tmp = mArray[offset][offset:]
                        for j in xrange(offset, width):
                            mArray[j][offset] = mArray[j][i]
                            mArray[j][i] = tmp[j]
                        # mArray[offset][offset:] = mArray[i][offset:]
                        # mArray[i] = tmp
                        break

            currentRow = [mArray[j][offset] for j in xrange(offset, width)]
            devider = float(currentRow[0])
            # If no line is found with an value != 0
            # the matrix is not invertible
            if devider == 0:
                raise ValueError("Matrix is not invertible")
            transformedRow = []
            # Devide current row by first element of current row
            for value in currentRow:
                transformedRow.append(value / devider)
            # put transformed row back into matrix
            for j in xrange(offset, width):
                mArray[j][offset] = transformedRow[j - offset]
            # subtract multiples of the current row, from all remaining rows
            # in order to become a 0 at the current first column
            for i in xrange(offset + 1, height):
                multi = mArray[offset][i]
                for j in xrange(offset, width):
                    mArray[j][i] = mArray[j][i] - mArray[j][offset] * multi
        for i in xrange(1, height):
            # subtract multiples of the i-the row from all above rows
            for j in xrange(0, i):
                multi = mArray[i][j]
                for col in xrange(i, width):
                    mArray[col][j] = mArray[col][j] - mArray[col][i] * multi
        self.matrix = mArray
        return self

    def __add__(self, matrix):
        """Return a new Matrix instance with the result of the addition

        :param Matrix matrix: The matrix, which should be added to the instance
        :return: A new Matrix with the same size with the result of the addition
        :rtype: Matrix

        :raise: Raises a :py:exc:`ValueError` if the size of the instance does
                not match with the size of the parameter matrix
        """
        if self.get_height() != matrix.get_height() or self.get_width() != matrix.get_width():
            raise ValueError("Size of matrix does not match")
        result = Matrix(self.get_width(), self.get_height())
        for row in xrange(self.get_height()):
            for col in xrange(self.get_width()):
                result.set_value(col, row, self.get_value(col, row) + matrix.get_value(col, row))
        return result

    def __sub__(self, matrix):
        """Return a new Matrix instance with the result of the subtraction

        :param Matrix matrix: The matrix, which should be subtracted from the instance
        :return: A new Matrix with the same size with the result of the subtraction
        :rtype: Matrix

        :raise: Raises a :py:exc:`ValueError` if the size of the instance does
                not match with the size of the parameter matrix
        """
        if self.get_height() != matrix.get_height() or self.get_width() != matrix.get_width():
            raise ValueError("Size of matrix does not match")
        result = Matrix(self.get_width(), self.get_height())
        for row in xrange(self.get_height()):
            for col in xrange(self.get_width()):
                result.set_value(col, row, self.get_value(col, row) - matrix.get_value(col, row))
        return result

    def __div__(self, divider):
        """Return a new Matrix, where all values are divided by the divider

        :param integer divider: The divider to divide all values of the matrix

        :return:    A new Matrix, where all values are divided by the divider
        :rtype: Matrix
        """
        result = Matrix(self.get_width(), self.get_height())
        for row in xrange(self.get_height()):
            for col in xrange(self.get_width()):
                result.set_value(col, row, self.get_value(col, row) / float(divider))
        return result

    def householder(self):
        """Return Matrices u,b,v with self = ubv and b is in bidiagonal form

        The algorithm uses householder transformations.

        :return tuple (u,b,v): A tuple with the Matrix u, b and v.
                and self = ubv (except some rounding errors)
                u is a unitary matrix
                b is a bidiagonal matrix.
                v is a unitary matrix.
        :note: Currently the algorithm only works for squared matrices

        :todo: Make sure, that the bidiagonal matrix is 0.0 except for the bidiagonal.
            Due to rounding errors, this is currently not ensured
        """
        # copy instance to transform it to bidiagonal form.
        bidiagMatrix = Matrix.from_two_dim_array(self.get_width(), self.get_height(), self.matrix)

        # build identity matrix, which is used to calculate householder transformations
        identityMatrixRow = Matrix(self.get_height(), self.get_height())
        for i in xrange(self.get_height()):
            identityMatrixRow.set_value(i, i, 1.0)

        identityMatrixCol = Matrix(self.get_width(), self.get_width())
        for i in xrange(self.get_width()):
            identityMatrixCol.set_value(i, i, 1.0)

        # zero out the k'th column and row
        for k in xrange(self.get_width() - 1):
            # vector with the values of the k'th column (first k-1 rows are 0)
            x = Vector(self.get_height())
            y = Vector(self.get_height())
            if k > 0:
                x.set_value(0, k - 1, bidiagMatrix.get_value(k, k - 1))
                y.set_value(0, k - 1, bidiagMatrix.get_value(k, k - 1))
            s = 0.0
            for i in xrange(k, self.get_height()):
                val = bidiagMatrix.get_value(k, i)
                x.set_value(0, i, val)
                s += (val ** 2)
            s = sqrt(s)
            # y must have same length as x
            y.set_value(0, k, s)
            tmp = x - y
            norm = sqrt(sum(i[0] ** 2 for i in tmp.get_array()))
            # calculate w = (x-y)/(|x-y|)
            w = tmp / norm
            # uk is the k'th householder matrix for the column
            uk = identityMatrixRow - 2 * (w * w.transform())

            bidiagMatrix = uk * bidiagMatrix

            if k == 0:
                # set u in first iteration.
                u = uk
            else:
                u = u * uk

            # zero out the the row
            if k < self.get_width() - 2:
                x = Vector(self.get_width())
                y = Vector(self.get_width())
                x.set_value(0, k, bidiagMatrix.get_value(k, k))
                y.set_value(0, k, bidiagMatrix.get_value(k, k))

                s = 0.0
                for i in xrange(k + 1, bidiagMatrix.get_width()):
                    val = bidiagMatrix.get_value(i, k)
                    x.set_value(0, i, val)
                    s += (val ** 2)
                # length of vector x ignoring the k'th value
                s = sqrt(s)
                # y must have same length as x, since k'th value is equal
                # set k+1 value to s
                y.set_value(0, k + 1, s)
                tmp = x - y
                norm = sqrt(sum(i[0] ** 2 for i in tmp.get_array()))
                w = tmp / norm
                # vk is the k'th householder matrix for the row
                vk = identityMatrixCol - (2 * (w * w.transform()))
                bidiagMatrix = bidiagMatrix * vk
                if k == 0:
                    # set v in first iteration
                    v = vk
                else:
                    v = vk * v

        return (u, bidiagMatrix, v)

    def svd(self, maxIteration=50):
        """Return the singular value decomposition of the Matrix instance

        :param integer maxIteration: The maximmum number of iterations,
            which are executed in the qr decomposition

        :return: A tuple with Matrices u, sigma, v with
                    so that u * sigma * v^T = self
        :rtype: tuple

        :raise: Raises a :py:exc:`ValueError` if the Matrix object has
                    more columns than rows

        :note:  Translation of the FORTRAN implementation if the SVD given
                in the NUMERICAL RECIPES IN FORTRAN 77. THE ART OF SCIENTIFIC
                COMPUTING.
                The algorithm is not yet numerical stable, so the results may
                not be in all cases as expected.
        """
        if(self.get_width() > self.get_height()):
            raise ValueError("Matrix has more columns than rows.")
        eps = 1.e-15
        tol = 1.e-64 / eps
        a = self.get_array(False)
        m = len(a[0])
        n = len(a)

        v = []
        for k in xrange(n):
            v.append([0.0] * n)
        # output diagonal
        w = [0.0] * n
        # upper diagonal (for bidiagonal form)
        rv1 = [0.0] * n

        # Householder Reduction to bidiagional form
        g = 0.0
        anorm = 0.0

        for i in xrange(n):
            l = i + 1
            rv1[i] = g

            s = 0.0
            # calculate length of relevant row vector in matrix (part of i'th column)
            s = sum(a[i][k] ** 2 for k in xrange(i, m))
            if s <= tol:
                g = 0.0
            else:
                f = a[i][i]
                # square root to get actual length of vector
                g = sqrt(s) if f < 0 else -sqrt(s)
                h = f * g - s
                a[i][i] = f - g
                for j in xrange(l, n):
                    s = sum(a[i][k] * a[j][k] for k in xrange(i, m))
                    f = s / h
                    for k in xrange(i, m):
                        a[j][k] += (f * a[i][k])
            w[i] = g
            # calculate length of relevant column vector in matrix (part of i'th row)
            s = 0.0
            s = sum(a[k][i] ** 2 for k in xrange(l, n))
            if s <= tol:
                g = 0.0
            else:
                f = a[l][i]
                g = sqrt(s) if f < 0 else -sqrt(s)
                h = f * g - s
                a[l][i] = f - g
                for k in xrange(l, n):
                    rv1[k] = a[k][i] / h
                for j in xrange(l, m):
                    s = sum(a[k][j] * a[k][i] for k in xrange(l, n))
                    for k in xrange(l, n):
                        a[k][j] += (s * rv1[k])
            anorm = max(anorm, (abs(w[i]) + abs(rv1[i])))

        ## Accumulation of right hand transformations
        for i in xrange(n - 1, -1, -1):
            if g != 0.0:
                for j in xrange(l, n):
                    v[i][j] = a[j][i] / (g * a[i + 1][i])
                for j in xrange(l, n):
                    s = sum(a[k][i] * v[j][k] for k in xrange(l, n))
                    for k in xrange(l, n):
                        v[j][k] += (s * v[i][k])
            for j in xrange(l, n):
                v[j][i] = 0.0
                v[i][j] = 0.0
            v[i][i] = 1.0
            g = rv1[i]
            l = i

        ## Accumulation of left hand transformations
        for i in xrange(n - 1, -1, -1):
            l = i + 1
            g = w[i]
            for j in xrange(l, n):
                a[j][i] = 0.0
            if g != 0.0:
                for j in xrange(l, n):
                    s = sum(a[i][k] * a[j][k] for k in xrange(l, m))
                    f = s / (a[i][i] * g)
                    for k in xrange(i, m):
                        a[j][k] += f * a[i][k]
                for j in xrange(i, m):
                    a[i][j] /= g
            else:
                for j in xrange(i, m):
                    a[i][j] = 0.0
            a[i][i] += 1.0

        eps *= anorm

        # Diagonalization of the bidiagonal form.
        # Loop over singular values and over allowed iterations
        for k in xrange(n - 1, -1, -1):
            for dummy in xrange(maxIteration):
                for l in xrange(k, -1, -1):
                    convergenceTest = False
                    if abs(rv1[l]) <= eps:
                        convergenceTest = True
                        break
                    if abs(w[l - 1]) <= eps:
                        # convergenceTest = False (already default)
                        break
                if not convergenceTest:
                    c = 0.0
                    s = 1.0
                    nm = l - 1
                    for i in xrange(l, k + 1):
                        f = s * rv1[i]
                        rv1[i] = c * rv1[i]
                        if abs(f) <= eps:
                            break
                        g = w[i]
                        h = pythag(f, g)
                        w[i] = h
                        c = g / h
                        s = -f / h
                        for j in xrange(m):
                            y = a[nm][j]
                            z = a[i][j]
                            a[nm][j] = (y * c) + (z * s)
                            a[i][j] = -(y * s) + (z * c)
                z = w[k]
                if l == k:
                    # convergence
                    if z < 0.0:
                        w[k] = -z
                        for j in xrange(n):
                            v[k][j] = -v[k][j]
                    break

                x = w[l]
                y = w[k - 1]
                g = rv1[k - 1]
                h = rv1[k]
                f = ((y - z) * (y + z) + (g - h) * (g + h)) / (2.0 * h * y)
                g = pythag(f, 1.0)
                f = ((x - z) * (x + z) + h * ((y / (f + sign(g, f))) - h)) / x
                c = 1.0
                s = 1.0
                for i in xrange(l + 1, k + 1):
                    g = rv1[i]
                    y = w[i]
                    h = s * g
                    g = c * g
                    z = pythag(f, h)
                    rv1[i - 1] = z
                    c = f / z
                    s = h / z
                    f = (x * c) + (g * s)
                    g = -x * s + g * c
                    h = y * s
                    y = y * c
                    for jj in xrange(n):
                        x = v[i - 1][jj]
                        z = v[i][jj]
                        v[i - 1][jj] = (x * c) + (z * s)
                        v[i][jj] = -(x * s) + (z * c)
                    z = pythag(f, h)
                    w[i - 1] = z
                    if z != 0.0:
                        z = 1.0 / z
                        c = f * z
                        s = h * z
                    f = (c * g) + (s * y)
                    x = -s * g + c * y
                    for jj in xrange(m):
                        y = a[i - 1][jj]
                        z = a[i][jj]
                        a[i - 1][jj] = (y * c) + (z * s)
                        a[i][jj] = -(y * s) + (z * c)
                rv1[l] = 0.0
                rv1[k] = f
                w[k] = x
        # Build Matrix instances for the result
        uM = Matrix.from_two_dim_array(len(a), len(a[0]), a)

        diagMatrix = Matrix(len(w), len(w))
        for i in xrange(len(w)):
            diagMatrix.set_value(i, i, w[i])

        vM = Matrix.from_two_dim_array(len(v), len(v[0]), v)

        return uM, diagMatrix, vM

    def pseudoinverse(self):
        """Return the pseudoinverse (Moore-Penrose-Inverse).

        The singular value decomposition is used to calculate the pseudoinverse.
        """
        transform = False
        if self.get_width() > self.get_height():
            transform = True
            u, sigma, v = self.transform().svd()
        else:
            u, sigma, v = self.svd()
        # calculate inverse of sigma
        for i in xrange(min(sigma.get_height(), sigma.get_width())):
            val = sigma.get_value(i, i)
            # divide only if the value is not 0 or close to zero (rounding errors)
            eps = 1.e-15
            if eps < val or val < -eps:
                sigma.set_value(i, i, 1 / val)
        if transform:
            return (v * sigma * u.transform()).transform()
        else:
            return v * sigma * u.transform()


class Vector(Matrix):
    """A vector instance is a Matrix, which only has 1 column"""

    def __init__(self, rows):
        """Initiliate a vector with the given number of rows.

        All values of this vector are 0.0"""
        super(Vector, self).__init__(1, rows)

    @classmethod
    def initialize_from_matrix(cls, matrix, column):
        """Create vector from matrix

        :param Matrix matrix: The Matrix, which should be used to create the vector.
        :param integer column: The column of the matrix, which should be used
                                to create the new vector.
        :raise: Raises an :py:exc:`IndexError` if the matrix does not have the specified column.
        """
        vec = Vector(matrix.get_height())
        for row in xrange(matrix.get_height()):
            vec.set_value(0, row, matrix.get_value(column, row))
        return vec

    def norm(self):
        """Calculates the norm (length) of the vector

        :return: Return the length of the vector
        :rtype: float
        """
        return sqrt(sum(i[0] ** 2 for i in self.get_array()))

    def unify(self):
        """Unifies the vector. The length of the vector will be 1.

        :return: Return the instance itself
        :rtype: Vector
        """
        length = float(self.norm())
        for row in xrange(self.get_height()):
            self.set_value(0, row, self.get_value(0, row) / length)
        return self
