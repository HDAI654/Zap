import re
from typing import Dict, Any

class PromptCompiler:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.operations = {
            'AR': self._add_row,
            'DR': self._delete_row,
            'EC': self._edit_cell,
            'AC': self._add_column,
            'DC': self._delete_column
        }
        self.patterns = {
            'AR': r'AR\s*\[([^\]]+)\]',
            'DR': r'DR\s*(\d+)',
            'EC': r'EC\s*\((\d+)\s*,\s*([^)]+)\)\s*"([^"]*)"',
            'AC': r'AC\s*"([^"]*)"',
            'DC': r'DC\s*"([^"]*)"'
        }

    def compile(self, prompt: str) -> Dict[str, Any]:
        """Main method to compile and execute prompts"""
        try:
            # Normalize prompt
            prompt = prompt.strip().upper()
            
            # Identify operation
            op_code = prompt[:2]
            if op_code not in self.operations:
                raise ValueError(f"Invalid operation code: {op_code}")
            
            # Extract arguments
            print(self.patterns[op_code])
            match = re.match(self.patterns[op_code], prompt[2:])
            print(match)
            
            # Execute operation
            result = self.operations[op_code](*match.groups())
            return {
                'status': 'success',
                'operation': op_code,
                'data': self.data,
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'data': self.data
            }

    def _add_row(self, values_str: str) -> str:
        """Add a new row with specified values"""
        values = [v.strip() for v in values_str.split(',')]
        
        # Validate column count
        col_count = len(self.data['data'])
        if len(values) != col_count:
            raise ValueError(f"Expected {col_count} values, got {len(values)}")
        
        # Add values to each column
        for i, (col_name, col_data) in enumerate(self.data['data'].items()):
            try:
                # Try to convert to number if possible
                value = float(values[i]) if values[i] and values[i].replace('.', '').isdigit() else values[i]
                col_data.append(value)
            except IndexError:
                col_data.append('')  # Default empty value
        
        return f"Added row with values: {values}"

    def _delete_row(self, row_index: str) -> str:
        """Delete a row by index"""
        idx = int(row_index)
        col_lengths = [len(col) for col in self.data['data'].values()]
        
        # Validate index
        if not col_lengths:
            raise ValueError("No columns exist")
        if len(set(col_lengths)) != 1:
            raise ValueError("Columns have inconsistent lengths")
        if idx < 0 or idx >= col_lengths[0]:
            raise ValueError(f"Row index {idx} out of range")
        
        # Delete from all columns
        for col_data in self.data['data'].values():
            col_data.pop(idx)
        
        return f"Deleted row at index {idx}"

    def _edit_cell(self, row_idx: str, col_name: str, new_value: str) -> str:
        """Edit a specific cell"""
        row = int(row_idx)
        col_name = col_name.strip().lower()
        
        # Validate column exists
        if col_name not in self.data['data']:
            raise ValueError(f"Column '{col_name}' not found")
        
        # Validate row exists
        if row < 0 or row >= len(self.data['data'][col_name]):
            raise ValueError(f"Row index {row} out of range")
        
        # Update value
        try:
            # Try to convert to number if possible
            self.data['data'][col_name][row] = float(new_value) if new_value and new_value.replace('.', '').isdigit() else new_value
        except ValueError:
            self.data['data'][col_name][row] = new_value
        
        return f"Updated cell at ({row}, {col_name}) to '{new_value}'"

    def _add_column(self, col_name: str) -> str:
        """Add a new column"""
        if col_name in self.data['data']:
            raise ValueError(f"Column '{col_name}' already exists")
        
        # Initialize with empty values matching existing row count
        row_count = len(next(iter(self.data['data'].values()))) if self.data['data'] else 0
        self.data['data'][col_name] = ['' for _ in range(row_count)]
        
        return f"Added column '{col_name}'"

    def _delete_column(self, col_name: str) -> str:
        """Delete an existing column"""
        if col_name not in self.data['data']:
            raise ValueError(f"Column '{col_name}' not found")
        
        del self.data['data'][col_name]
        return f"Deleted column '{col_name}'"


# Example Usage
if __name__ == "__main__":
    # Initialize with sample data
    d = {"name": "Salaries", "data": {"month1": [1000, 2000], "month2": [1500, 2500]}}
    compiler = PromptCompiler(d)
    
    # Test operations
    print(compiler.compile("AR [3000, 3500]"))
    #print(compiler.compile("DR 1"))      
